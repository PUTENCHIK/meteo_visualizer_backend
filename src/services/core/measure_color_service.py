from typing import override
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import MeasureColor
from src.repositories import (
    MeasureColorRepository,
    MeasureRepository,
)
from src.schemas import CreateMeasureColorSchema, UpdateMeasureColorSchema
from src.services.abstractions.auditable_service import AuditableService
from src.utils.exceptions import (
    MaxMeasureColorsException,
    MeasureColorAlreadyExistsException,
    MeasureColorNotFoundException,
    MeasureNotFoundException,
)


class MeasureColorService(AuditableService[MeasureColor, MeasureColorRepository]):
    """
    Сервис цветов пользовательских параметров визуализации
    """

    MAX_COLORS: int = 8

    _measure_repo: MeasureRepository

    @property
    def measure_repo(self) -> MeasureRepository:
        return self._measure_repo

    def __init__(self, session: AsyncSession):
        super().__init__(MeasureColorRepository(session))
        self._measure_repo = MeasureRepository(session)

    @override
    async def get_by_id(self, id_, include_deleted=False) -> MeasureColor:
        color = await self.repository.get_by_id(id_, include_deleted)
        if not color:
            raise MeasureColorNotFoundException(id_)
        return color

    async def create_measure_color(
        self, data: CreateMeasureColorSchema
    ) -> MeasureColor:
        measure = await self.measure_repo.get_by_id(data.measure_id)
        if not measure:
            raise MeasureNotFoundException(data.measure_id)
        
        if len(measure.colors) > self.MAX_COLORS:
            raise MaxMeasureColorsException(measure.name, self.MAX_COLORS)

        by_percent = await self.repository.get_by_percent(data.measure_id, data.percent)
        if by_percent:
            raise MeasureColorAlreadyExistsException(measure.name, data.percent)

        new_color = MeasureColor(**data.model_dump())

        return await self._create(new_color)

    async def update_measure_color(
        self, id_: UUID, data: UpdateMeasureColorSchema
    ) -> MeasureColor:
        color = await self.get_by_id(id_)

        if data.percent:
            by_percent = await self.repository.get_by_percent(
                color.measure_id, data.percent
            )
            if by_percent and by_percent.id != id_:
                raise MeasureColorAlreadyExistsException(
                    color.measure.name, data.percent
                )

        return await self._update(color, data)

    async def delete_measure_color(self, id_: UUID):
        color = await self.get_by_id(id_)

        await self._delete(color, force=True)
