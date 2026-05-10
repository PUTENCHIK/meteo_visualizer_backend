from typing import Dict, List
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.enums import SystemPermission
from src.config import config
from src.managers import InitialDataManager, PasswordManager
from src.models import Permission, Role, RolePermission, User
from src.repositories import (
    PermissionRepository,
    RolePermissionRepository,
    RoleRepository,
    UserRepository,
)
from src.schemas import (
    InitialRoleSchema,
    InitialUserSchema,
)
from src.utils.exceptions import (
    PermissionNotFoundException,
    RoleNotFoundException,
)


class InitialDataService:
    """
    Сервис данных инициализации
    """

    _role_repo: RoleRepository
    _permission_repo: PermissionRepository
    _role_permission_repo: RolePermissionRepository
    _user_repo: UserRepository
    _initial_data_manager: InitialDataManager = InitialDataManager()
    _password_manager: PasswordManager = PasswordManager()

    @property
    def role_repo(self) -> RoleRepository:
        return self._role_repo

    @property
    def permission_repo(self) -> PermissionRepository:
        return self._permission_repo

    @property
    def role_permission_repo(self) -> RolePermissionRepository:
        return self._role_permission_repo

    @property
    def user_repo(self) -> UserRepository:
        return self._user_repo

    @property
    def initial_data_manager(self) -> InitialDataManager:
        return self._initial_data_manager

    @property
    def password_manager(self) -> PasswordManager:
        return self._password_manager

    def __init__(self, session: AsyncSession):
        self._role_repo = RoleRepository(session)
        self._permission_repo = PermissionRepository(session)
        self._role_permission_repo = RolePermissionRepository(session)
        self._user_repo = UserRepository(session)

    async def generate_permissions(self):
        db_permissions = await self.permission_repo.get_all(include_deleted=True)
        db_names = set(perm.name for perm in db_permissions)

        enum_names = set(perm.value for perm in SystemPermission)
        to_add = enum_names - db_names

        permissions: List[Permission] = list()
        for permission in to_add:
            permissions.append(
                Permission(
                    name=permission,
                    description=permission,
                )
            )

        await self.permission_repo.add_many(permissions)
        await self.permission_repo.flush()

    async def generate_roles(self, data: List[InitialRoleSchema]):
        roles_dict: Dict[str, UUID] = dict()
        permissions_dict: Dict[SystemPermission, UUID] = dict()

        for initial_role in data:
            # Роли ожидаемо нет в словаре
            if initial_role.name not in roles_dict:
                role_by_name = await self.role_repo.get_by_name(
                    initial_role.name, include_deleted=True
                )
                # Роль есть в бд, скипаем
                if role_by_name is not None:
                    continue
            # Роль уже была добавлена, скипаем
            else:
                continue

            # Если родительская роль не загружена
            if (
                initial_role.parent_name is not None
                and initial_role.parent_name not in roles_dict
            ):
                parent_by_name = await self.role_repo.get_by_name(
                    initial_role.parent_name
                )
                # Если нет роли с именем, хотя должна быть
                if parent_by_name is None:
                    raise RoleNotFoundException(name=initial_role.parent_name)
                roles_dict[parent_by_name.name] = parent_by_name.id

            # добавление роли
            new_role = Role(
                name=initial_role.name,
                parent_id=(
                    roles_dict[initial_role.parent_name]
                    if initial_role.parent_name is not None
                    else None
                ),
            )
            new_role = await self.role_repo.add(new_role)
            await self.role_repo.flush()
            roles_dict[new_role.name] = new_role.id

            links_to_add: List[RolePermission] = list()
            for permission in initial_role.permissions:
                # если разрешение не подгружено
                if permission not in permissions_dict:
                    db_permission = await self.permission_repo.get_by_name(
                        permission.value
                    )
                    # разрешение обязано быть в базе
                    if db_permission is None:
                        raise PermissionNotFoundException(name=permission.value)
                    permissions_dict[permission.value] = db_permission.id

                links_to_add.append(
                    RolePermission(
                        role_id=roles_dict[new_role.name],
                        permission_id=permissions_dict[permission.value],
                    )
                )

            await self.role_permission_repo.add_many(links_to_add)
            await self.role_permission_repo.flush()

    async def generate_users(self, data: List[InitialUserSchema]):
        roles_dict: Dict[str, UUID] = dict()
        users_to_add: List[User] = list()

        password_hash = self.password_manager.hash_password(
            config.initial_users_password
        )

        for initial_user in data:
            if initial_user.role_name not in roles_dict:
                role = await self.role_repo.get_by_name(initial_user.role_name)
                if role is None:
                    raise RoleNotFoundException(name=initial_user.role_name)
                roles_dict[initial_user.role_name] = role.id

            user_by_login = await self.user_repo.get_by_login(initial_user.login)
            if user_by_login is not None:
                continue

            users_to_add.append(
                User(
                    **initial_user.model_dump(exclude={"role_name"}),
                    role_id=roles_dict[initial_user.role_name],
                    password_hash=password_hash,
                )
            )

        await self.user_repo.add_many(users_to_add)
        await self.user_repo.flush()

    async def get_base_role(self, name: str) -> Role:
        role = await self.role_repo.get_by_name(name)
        if role is None:
            raise RoleNotFoundException(name=name)

        return role

    async def save(self):
        await self.role_repo.commit()
        await self.permission_repo.commit()
        await self.role_permission_repo.commit()

    async def sync(self):
        await self.generate_permissions()

        init_data = self.initial_data_manager.initial_data

        if len(init_data.roles) > 0:
            await self.generate_roles(init_data.roles)

        if len(init_data.users) > 0:
            await self.generate_users(init_data.users)

        base_role = await self.get_base_role(init_data.base_role_name)
        self.initial_data_manager.base_role_id = base_role.id

        await self.save()
