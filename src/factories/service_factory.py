from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db import get_session
from src.repositories import (RoleRepository, UserRepository, 
                              PermissionRepository, RolePermissionRepository)
from src.services import AuthService, RoleService, PermissionService


class ServiceFactory:
    """
    Фабрика для генерации сервисов приложения
    """

    @staticmethod
    async def get_auth_service(session: AsyncSession = Depends(get_session)):
        return AuthService(UserRepository(session))

    @staticmethod
    async def get_role_service(session: AsyncSession = Depends(get_session)):
        return RoleService(
            RoleRepository(session),
            PermissionRepository(session),
            RolePermissionRepository(session)
        )
    
    @staticmethod
    async def get_permission_service(session: AsyncSession = Depends(get_session)):
        return PermissionService(PermissionRepository(session))
