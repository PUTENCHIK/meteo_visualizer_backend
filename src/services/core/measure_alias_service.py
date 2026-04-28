from typing import override
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import MeasureAlias
from src.repositories import (
    MeasureAliasRepository,
    MeasureRepository,
)
from src.schemas import CreateMeasureAliasSchema, UpdateMeasureAliasSchema
from src.services.abstractions.auditable_service import AuditableService
from src.utils.exceptions import (
    MeasureAliasAlreadyExistsException,
    MeasureAliasNotFoundException,
    MeasureNotFoundException,
)


class MeasureAliasService(AuditableService[MeasureAlias, MeasureAliasRepository]):
    """
    Сервис псевдонимов пользовательских параметров визуализации
    """

    _measure_repo: MeasureRepository

    @property
    def measure_repo(self) -> MeasureRepository:
        return self._measure_repo

    def __init__(self, session: AsyncSession):
        super().__init__(MeasureAliasRepository(session))
        self._measure_repo = MeasureRepository(session)

    @override
    async def get_by_id(self, id_, include_deleted=False) -> MeasureAlias:
        alias = await self.repository.get_by_id(id_, include_deleted)
        if not alias:
            raise MeasureAliasNotFoundException(id_)
        return alias

    async def create_measure_alias(
        self, data: CreateMeasureAliasSchema
    ) -> MeasureAlias:
        measure = await self.measure_repo.get_by_id(data.measure_id)

        if not measure:
            raise MeasureNotFoundException(data.measure_id)

        by_name = await self.repository.get_by_name(data.measure_id, data.name)
        if by_name:
            raise MeasureAliasAlreadyExistsException(measure.name, data.name)

        new_alias = MeasureAlias(**data.model_dump())

        return await self._create(new_alias)

    async def update_measure_alias(
        self, id_: UUID, data: UpdateMeasureAliasSchema
    ) -> MeasureAlias:
        alias = await self.get_by_id(id_)

        if data.name:
            by_name = await self.repository.get_by_name(alias.measure_id, data.name)
            if by_name and by_name.id != id_:
                raise MeasureAliasAlreadyExistsException(alias.measure.name, data.name)

        return await self._update(alias, data)

    async def delete_measure_alias(self, id_: UUID):
        alias = await self.get_by_id(id_)

        await self._delete(alias, force=True)
