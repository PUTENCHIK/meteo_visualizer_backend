from typing import List, override
from uuid import UUID

from src.models import Role, RolePermission
from src.repositories import (
    PermissionRepository,
    RolePermissionRepository,
    RoleRepository,
)
from src.schemas import (
    AddPermissionToRoleSchema,
    CreateRolePermissionSchema,
    CreateRoleSchema,
    DeletePermissionToRoleSchema,
    UpdateRoleSchema,
)
from src.services.abstractions.auditable_service import AuditableService
from src.utils.exceptions import (
    PermissionNotFoundException,
    RoleHasChildrenException,
    RoleHasUsersException,
    RoleNameAlreadyExistsException,
    RoleNotDeletedException,
    RoleNotFoundException,
    RoleParentCantBeSameException,
)


class RoleService(AuditableService[Role, RoleRepository]):
    """
    Сервис ролей пользователей
    """

    __perm_repository: PermissionRepository
    __role_perm_repository: RolePermissionRepository

    @property
    def role_perm_repository(self) -> RolePermissionRepository:
        return self.__role_perm_repository

    def __init__(
        self,
        repository: RoleRepository,
        p_repo: PermissionRepository,
        rp_repo: RolePermissionRepository,
    ):
        super().__init__(repository)
        self.__perm_repository = p_repo
        self.__role_perm_repository = rp_repo

    @override
    async def get_by_id(self, id_, include_deleted=False) -> Role:
        role = await self._repository.get_by_id(id_, include_deleted)
        if not role:
            raise RoleNotFoundException(id_)
        return role

    async def get_role_with_permissions(self, id_: UUID) -> Role:
        role = await self.get_by_id(id_)
        permissions = await self._repository.get_all_permissions(role.id)
        role.permissions = permissions

        return role

    async def get_all_with_permissions(
        self, include_deleted: bool = False
    ) -> List[Role]:
        roles = await self._repository.get_all(include_deleted)
        perms_map = await self._repository.get_all_with_permissions(include_deleted)

        for role in roles:
            role.permissions = perms_map.get(role.id, [])

        return roles

    async def create_role(self, data: CreateRoleSchema) -> Role:
        role = await self._repository.get_by_name(data.name)
        if role:
            raise RoleNameAlreadyExistsException(data.name, role.deleted_at is not None)

        new_role = Role(
            name=data.name,
            parent_id=data.parent_id,
        )
        if data.id is not None:
            new_role.id = data.id

        return await self._create(new_role)

    async def generate_role(self, data: CreateRoleSchema) -> Role:
        role = await self._repository.get_by_id(data.id, include_deleted=True)

        if role:
            if role.deleted_at is not None:
                await self._repository.restore(role)
            return role

        by_name = await self._repository.get_by_name(data.name, include_deleted=True)
        if by_name:
            if by_name.deleted_at is not None:
                await self._repository.restore(role)
            return role

        new_role = Role(
            id=data.id,
            name=data.name,
            parent_id=data.parent_id,
        )
        await self._repository.add(new_role)
        return new_role

    async def generate_role_permission(
        self, data: CreateRolePermissionSchema, check_role_exists: bool = False
    ) -> RolePermission:
        if check_role_exists:
            await self.get_by_id(data.role_id)
        permission = await self.__perm_repository.get_by_name(data.permission.value)
        if not permission:
            raise PermissionNotFoundException(name=data.permission.value)
        link = await self.__role_perm_repository.get_by_ids(data.role_id, permission.id)
        if not link:
            link = RolePermission(
                role_id=data.role_id, permission_id=permission.id, creator_id=None
            )
            await self.__role_perm_repository.add(link)

        return link

    async def create_roles_permissions(
        self, role_id: UUID, data: List[AddPermissionToRoleSchema]
    ) -> List[RolePermission]:
        await self.get_by_id(role_id)

        links: List[RolePermission] = list()
        for link_data in data:
            links.append(
                await self.generate_role_permission(
                    CreateRolePermissionSchema(
                        role_id=role_id, permission=link_data.permission
                    )
                )
            )

        await self.__role_perm_repository.commit()
        for link in links:
            await self.__role_perm_repository.refresh(link)

        return links

    async def delete_roles_permissions(
        self, role_id: UUID, data: List[DeletePermissionToRoleSchema]
    ):
        await self.get_by_id(role_id)
        for link_data in data:
            permission = await self.__perm_repository.get_by_name(
                link_data.permission.value
            )
            if not permission:
                raise PermissionNotFoundException(name=link_data.permission.value)
            link = await self.__role_perm_repository.get_by_ids(role_id, permission.id)
            if link:
                await self.__role_perm_repository.delete(link)

        await self.__role_perm_repository.commit()

    async def restore_role(self, id_: UUID) -> Role:
        role = await self.get_by_id(id_, include_deleted=True)

        if role.deleted_at is None:
            raise RoleNotDeletedException(id_)

        return await self._restore(role)

    async def update_role(self, id_: UUID, data: UpdateRoleSchema) -> Role:
        role = await self.get_by_id(id_)

        if data.name is not None:
            by_name = await self._repository.get_by_name(data.name)
            if by_name:
                raise RoleNameAlreadyExistsException(data.name)

        if data.parent_id == id_:
            raise RoleParentCantBeSameException()

        return await self._repository.update(role, data)

    async def delete_role(self, id_: UUID, force: bool = False):
        role = await self.get_by_id(id_)

        if len(role.children) > 0:
            raise RoleHasChildrenException(id_, len(role.children))

        if len(role.users) > 0:
            raise RoleHasUsersException(id_, len(role.users))

        await self._delete(role, force)
