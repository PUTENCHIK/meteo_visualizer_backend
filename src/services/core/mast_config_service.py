from typing import override
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import MastConfig
from src.repositories import MastConfigRepository
from src.schemas import CreateMastConfigSchema, UpdateMastConfigSchema
from src.services.abstractions.auditable_service import AuditableService
from src.utils.exceptions import (
    MastConfigNotDeletedException,
    MastConfigNotFoundException,
)


class MastConfigService(AuditableService[MastConfig, MastConfigRepository]):
    """
    Сервис конфигов мачт
    """

    def __init__(self, session: AsyncSession):
        super().__init__(MastConfigRepository(session))

    @override
    async def get_by_id(self, id_, include_deleted=False) -> MastConfig:
        config = await self.repository.get_by_id(id_, include_deleted)
        if not config:
            raise MastConfigNotFoundException(id_)
        return config

    async def create_mast_config(self, data: CreateMastConfigSchema) -> MastConfig:
        new_config = MastConfig(**data.model_dump())

        return await self._create(new_config)

    async def restore_mast_config(self, id_: UUID) -> MastConfig:
        config = await self.get_by_id(id_, include_deleted=True)

        if config.deleted_at is None:
            raise MastConfigNotDeletedException(id_)

        return await self._restore(config)

    async def update_mast_config(
        self, id_: UUID, data: UpdateMastConfigSchema
    ) -> MastConfig:
        config = await self.get_by_id(id_)

        return await self._update(config, data)

    async def delete_mast_config(self, id_: UUID, force: bool = False):
        config = await self.get_by_id(id_)

        # TODO: удалить связанные реи, проверить существование мачт

        await self._delete(config, force)
