from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db import get_session
from src.services import (
    AuthService,
    ComplexService,
    MastConfigService,
    MastService,
    MastYardService,
    PermissionService,
    RoleService,
    UserService,
)


class ServiceFactory:
    """
    Фабрика для генерации сервисов приложения
    """

    @staticmethod
    async def get_auth_service(session: AsyncSession = Depends(get_session)):
        return AuthService(session)

    @staticmethod
    async def get_role_service(session: AsyncSession = Depends(get_session)):
        return RoleService(session)

    @staticmethod
    async def get_permission_service(session: AsyncSession = Depends(get_session)):
        return PermissionService(session)

    @staticmethod
    async def get_user_service(session: AsyncSession = Depends(get_session)):
        return UserService(session)

    @staticmethod
    async def get_complex_service(session: AsyncSession = Depends(get_session)):
        return ComplexService(session)

    @staticmethod
    async def get_mast_service(session: AsyncSession = Depends(get_session)):
        return MastService(session)

    @staticmethod
    async def get_mast_config_service(session: AsyncSession = Depends(get_session)):
        return MastConfigService(session)

    @staticmethod
    async def get_mast_yard_service(session: AsyncSession = Depends(get_session)):
        return MastYardService(session)
