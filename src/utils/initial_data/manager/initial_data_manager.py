from src.utils import SingletonMetaclass
from sqlalchemy.ext.asyncio import AsyncSession
from src.factories import ServiceFactory
from src.utils.permissions import SystemPermission
from src.schemas import CreatePermissionSchema

from src.utils.initial_data.data.roles import INITIAL_ROLES
from src.utils.initial_data.data.roles_permissions import INITIAL_ROLES_PERMISSIONS


class InitialDataManager(metaclass=SingletonMetaclass):
    """
    Менеджер-сингтон для синхронизации данных инициализации с базой данных
    """

    def __init__(self):
        pass

    async def __sync_roles(self, session: AsyncSession):
        service = await ServiceFactory.get_role_service(session)

        for data in INITIAL_ROLES:
            await service.generate_role(data)
        
        await session.commit()

    async def __sync_permissions(self, session: AsyncSession):
        service = await ServiceFactory.get_permission_service(session)

        permissions = [p.value for p in SystemPermission]
        db_permissions = await service.get_all()
        db_names = [p.name for p in db_permissions]
        
        to_create = [name for name in permissions if name not in db_names]

        for name in to_create:
            await service.create_permission(
                data=CreatePermissionSchema(name=name, description=name))
        
    async def __sync_roles_permissions(self, session: AsyncSession):
        service = await ServiceFactory.get_role_service(session)

        for data in INITIAL_ROLES_PERMISSIONS:
            await service.generate_role_permission(data, check_role_exists=True)

        await session.commit()

    async def sync(self, session: AsyncSession):
        await self.__sync_roles(session)
        await self.__sync_permissions(session)
        await self.__sync_roles_permissions(session)