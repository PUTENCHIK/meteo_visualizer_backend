from typing import override
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import MastConfig
from src.repositories import MastConfigRepository, MastYardRepository
from src.schemas import CreateMastConfigSchema, UpdateMastConfigSchema
from src.services.abstractions.auditable_service import AuditableService
from src.utils.exceptions import (
    MastConfigHasActiveMastsException,
    MastConfigNotDeletedException,
    MastConfigNotFoundException,
    MastConfigTooLowException,
)


class MastConfigService(AuditableService[MastConfig, MastConfigRepository]):
    """
    Сервис конфигов мачт
    """

    _mast_yard_repo: MastYardRepository

    @property
    def mast_yard_repo(self) -> MastYardRepository:
        return self._mast_yard_repo

    def __init__(self, session: AsyncSession):
        super().__init__(MastConfigRepository(session))
        self._mast_yard_repo = MastYardRepository(session)

    @override
    async def get_by_id(self, id_, include_deleted=False) -> MastConfig:
        config = await self.repository.get_by_id(id_, include_deleted)
        if not config:
            raise MastConfigNotFoundException(id_)
        return config

    async def create_mast_config(self, data: CreateMastConfigSchema) -> MastConfig:
        new_config = MastConfig(**data.model_dump())
        new_config = await self._create(new_config)

        return await self.get_by_id(new_config.id)

    async def restore_mast_config(self, id_: UUID) -> MastConfig:
        config = await self.get_by_id(id_, include_deleted=True)

        if config.deleted_at is None:
            raise MastConfigNotDeletedException(id_)

        yards = await self.mast_yard_repo.get_by_config(id_, include_deleted=True)
        for yard in yards:
            await self.mast_yard_repo.restore(yard)

        return await self._restore(config)

    async def update_mast_config(
        self, id_: UUID, data: UpdateMastConfigSchema
    ) -> MastConfig:
        config = await self.get_by_id(id_)
        if data.height is not None:
            for yard in config.yards:
                if yard.height > data.height:
                    raise MastConfigTooLowException(yard.height)

        return await self._update(config, data)

    async def delete_mast_config(self, id_: UUID):
        config = await self.get_by_id(id_)

        if len(config.masts) > 0:
            raise MastConfigHasActiveMastsException(id_, len(config.masts))

        for yard in config.yards:
            await self.mast_yard_repo.delete(yard)

        await self._delete(config)
