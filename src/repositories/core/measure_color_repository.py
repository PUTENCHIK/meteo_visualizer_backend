from typing import List, Optional, override
from uuid import UUID

from sqlalchemy.orm import selectinload

from src.models import MeasureColor
from src.repositories.abstractions.auditable_repository import AuditableRepository


class MeasureColorRepository(AuditableRepository[MeasureColor]):
    """
    Репозиторий сущностей цветов пользовательских параметров визуализации
    """

    @override
    def __init__(self, session):
        super().__init__(MeasureColor, session)

    @override
    def _get_all_query(self, include_deleted: bool = False):
        statement = super()._get_all_query(include_deleted)
        return statement.options(
            selectinload(MeasureColor.measure),
        )

    async def get_by_measure(
        self, measure_id: UUID, include_deleted: bool = False
    ) -> List[MeasureColor]:
        statement = self._get_all_query(include_deleted).where(
            MeasureColor.measure_id == measure_id
        )
        result = await self.session.exec(statement)
        return result.all()

    async def get_by_percent(
        self,
        measure_id: UUID,
        percent: float,
    ) -> Optional[MeasureColor]:
        statement = self._get_all_query().where(
            MeasureColor.measure_id == measure_id, MeasureColor.percent == percent
        )
        result = await self.session.exec(statement)
        return result.one_or_none()
