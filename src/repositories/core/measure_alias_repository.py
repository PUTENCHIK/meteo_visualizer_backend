from typing import List, Optional, override
from uuid import UUID

from sqlalchemy.orm import selectinload

from src.models import MeasureAlias
from src.repositories.abstractions.auditable_repository import AuditableRepository


class MeasureAliasRepository(AuditableRepository[MeasureAlias]):
    """
    Репозиторий сущностей системных псевдонимов пользовательских параметров визуализации
    """

    @override
    def __init__(self, session):
        super().__init__(MeasureAlias, session)

    @override
    def _get_all_query(self, include_deleted: bool = False):
        statement = super()._get_all_query(include_deleted)
        return statement.options(
            selectinload(MeasureAlias.measure),
        )

    async def get_by_measure(
        self,
        measure_id: UUID,
        include_deleted: bool = False
    ) -> List[MeasureAlias]:
        statement = self._get_all_query(include_deleted).where(
            MeasureAlias.measure_id == measure_id
        )
        result = await self.session.exec(statement)
        return result.all()
    
    async def get_by_name(
        self,
        measure_id: UUID,
        name: str,
    ) -> Optional[MeasureAlias]:
        statement = self._get_all_query().where(
            MeasureAlias.measure_id == measure_id,
            MeasureAlias.name == name.lower()
        )
        result = await self.session.exec(statement)
        return result.one_or_none()
