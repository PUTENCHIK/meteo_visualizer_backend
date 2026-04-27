from typing import override
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import Measure, User
from src.repositories import (
    MeasureAliasRepository,
    MeasureColorRepository,
    MeasureRepository,
    UserRepository,
)
from src.schemas import (
    CreateMeasureSchema,
    UpdateMeasureSchema,
)
from src.services.abstractions.auditable_service import AuditableService
from src.utils.exceptions import (
    InvalidMeasureScaleException,
    MeasureNotDeletedException,
    MeasureNotFoundException,
)


class MeasureService(AuditableService[Measure, MeasureRepository]):
    """
    Сервис пользовательских параметров визуализации
    """

    _user_repo: UserRepository
    _measure_color_repo: MeasureColorRepository
    _measure_alias_repo: MeasureAliasRepository

    @property
    def user_repo(self) -> UserRepository:
        return self._user_repo
    
    @property
    def measure_color_repo(self) -> MeasureColorRepository:
        return self._measure_color_repo
    
    @property
    def measure_alias_repo(self) -> MeasureAliasRepository:
        return self._measure_alias_repo

    def __init__(self, session: AsyncSession):
        super().__init__(MeasureRepository(session))
        self._user_repo = UserRepository(session)
        self._measure_color_repo = MeasureColorRepository(session)
        self._measure_alias_repo = MeasureAliasRepository(session)
    
    @override
    async def get_by_id(self, id_, include_deleted=False) -> Measure:
        measure = await self.repository.get_by_id(id_, include_deleted)
        if not measure:
            raise MeasureNotFoundException(id_)
        return measure
    
    def validate_min_max(self, min: int, max: int) -> bool:
        if min >= max:
            raise InvalidMeasureScaleException(min, max)
        return True
    
    async def create_measure(self, data: CreateMeasureSchema, user: User) -> Measure:
        self.validate_min_max(data.min, data.max)

        new_measure = Measure(
            **data.model_dump(),
            creator_id=user.id,
        )
        new_measure = await self._create(new_measure)

        return await self.get_by_id(new_measure.id)
    
    async def restore_measure(self, id_: UUID) -> Measure:
        measure = await self.get_by_id(id_, include_deleted=True)

        if measure.deleted_at is None:
            raise MeasureNotDeletedException(id_)

        colors = await self.measure_color_repo.get_by_measure(id_, include_deleted=True)
        for color in colors:
            await self.measure_color_repo.restore(color)
        
        aliases = await self.measure_alias_repo.get_by_measure(
            id_,
            include_deleted=True
        )
        for alias in aliases:
            await self.measure_alias_repo.restore(alias)

        return await self._restore(measure)

    async def update_measure(
        self, id_: UUID, data: UpdateMeasureSchema
    ) -> Measure:
        measure = await self.get_by_id(id_)
        
        if data.min and data.max:
            self.validate_min_max(data.min, data.max)

        return await self._update(measure, data)
    
    async def delete_measure(self, id_: UUID, force: bool = False):
        measure = await self.get_by_id(id_)

        for color in measure.colors:
            await self.measure_color_repo.delete(color, force)
        for alias in measure.aliases:
            await self.measure_alias_repo.delete(alias, force)

        await self._delete(measure, force)
