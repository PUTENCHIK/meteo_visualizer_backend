from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db import get_session
from src.repositories import (
    PermissionRepository,
    RolePermissionRepository,
    RoleRepository,
    UserRepository,
)
from src.services import AuthService, PermissionService, RoleService, UserService


class ServiceFactory:
    """
    Фабрика для генерации сервисов приложения
    """

    @staticmethod
    async def get_auth_service(session: AsyncSession = Depends(get_session)):
        return AuthService(UserRepository(session), RoleRepository(session))

    @staticmethod
    async def get_role_service(session: AsyncSession = Depends(get_session)):
        return RoleService(
            RoleRepository(session),
            PermissionRepository(session),
            RolePermissionRepository(session),
        )

    @staticmethod
    async def get_permission_service(session: AsyncSession = Depends(get_session)):
        return PermissionService(PermissionRepository(session))

    @staticmethod
    async def get_user_service(session: AsyncSession = Depends(get_session)):
        return UserService(UserRepository(session), RoleRepository(session))
