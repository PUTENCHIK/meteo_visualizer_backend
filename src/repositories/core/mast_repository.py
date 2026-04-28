from typing import List, Optional, override
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import selectinload

from src.models import Mast, MastConfig, MastYard
from src.repositories.abstractions.auditable_repository import AuditableRepository


class MastRepository(AuditableRepository[Mast]):
    """
    Репозиторий сущностей мачт комплексов
    """

    @override
    def __init__(self, session):
        super().__init__(Mast, session)

    @override
    def _get_all_query(self, include_deleted: bool = False):
        statement = super()._get_all_query(include_deleted)
        return statement.options(
            selectinload(Mast.config).selectinload(
                MastConfig.yards.and_(MastYard.deleted_at.is_(None))
            ),
            selectinload(Mast.complex),
        )

    async def get_by_complex(
        self, complex_id: UUID, include_deleted: bool = False
    ) -> List[Mast]:
        statement = self._get_all_query(include_deleted).where(
            Mast.complex_id == complex_id
        )
        result = await self.session.exec(statement)
        return result.all()

    async def get_by_prefix(self, complex_id: UUID, prefix: str) -> Optional[Mast]:
        statement = self._get_all_query().where(
            Mast.complex_id == complex_id, func.lower(Mast.prefix) == prefix.lower()
        )
        result = await self.session.exec(statement)
        return result.one_or_none()
