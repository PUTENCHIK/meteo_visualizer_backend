from typing import List, override
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import Permission
from src.repositories import (
    PermissionRepository,
    RolePermissionRepository,
    RoleRepository,
)
from src.schemas import (
    CreatePermissionSchema,
    PermissionWithRoleInfoSchema,
    UpdatePermissionSchema,
)
from src.services.abstractions.auditable_service import AuditableService
from src.utils.exceptions import (
    PermissionNameAlreadyExistsException,
    PermissionNotDeletedException,
    PermissionNotFoundException,
    RoleNotFoundException,
)


class PermissionService(AuditableService[Permission, PermissionRepository]):
    """
    Сервис разрешений для ролей пользователей
    """

    _role_repo: RoleRepository
    _role_permission_repo: RolePermissionRepository

    @property
    def role_repo(self) -> RoleRepository:
        return self._role_repo

    @property
    def role_permission_repo(self) -> RolePermissionRepository:
        return self._role_permission_repo

    def __init__(self, session: AsyncSession):
        super().__init__(PermissionRepository(session))
        self._role_repo = RoleRepository(session)
        self._role_permission_repo = RolePermissionRepository(session)

    @override
    async def get_by_id(self, id_, include_deleted=False) -> Permission:
        permission = await self.repository.get_by_id(id_, include_deleted)
        if not permission:
            raise PermissionNotFoundException(id_)
        return permission

    async def get_all_with_relative_of_role(
        self, id_: UUID
    ) -> List[PermissionWithRoleInfoSchema]:
        role = await self.role_repo.get_by_id(id_)
        if not role:
            raise RoleNotFoundException(id_)

        permissions = await self.get_all()
        relative_ids = await self.role_permission_repo.get_relatives_to_role(
            role_id=role.id, permission_ids=[p.id for p in permissions]
        )
        ids_set = set(relative_ids)

        schemas = list()
        for permission in permissions:
            schema = PermissionWithRoleInfoSchema.model_validate(permission)
            schema.is_relative = permission.id in ids_set
            schemas.append(schema)
        return schemas

    async def create_permission(self, data: CreatePermissionSchema) -> Permission:
        permission = await self.repository.get_by_name(data.name, include_deleted=True)
        if permission:
            if permission.deleted_at is None:
                raise PermissionNameAlreadyExistsException(data.name)
            else:
                permission = await self.restore_permission(permission.id)
                return await self.update_permission(
                    permission.id, UpdatePermissionSchema(description=data.description)
                )

        new_perm = Permission(name=data.name, description=data.description)

        return await self._create(new_perm)

    async def restore_permission(self, id_: UUID) -> Permission:
        permission = await self.get_by_id(id_, include_deleted=True)

        if permission.deleted_at is None:
            raise PermissionNotDeletedException(id_)

        return await self._restore(permission)

    async def update_permission(
        self, id_: UUID, data: UpdatePermissionSchema
    ) -> Permission:
        permission = await self.get_by_id(id_)

        permission = await self.repository.update(permission, data)
        await self.repository.commit_refresh(permission)

        return permission

    async def delete_permission(self, id_: UUID, force: bool = False):
        permission = await self.get_by_id(id_)

        await self._delete(permission, force)
