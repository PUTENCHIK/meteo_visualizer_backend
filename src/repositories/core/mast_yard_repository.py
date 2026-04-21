from typing import List, Optional, override
from uuid import UUID

from sqlalchemy.orm import selectinload

from src.models import MastYard
from src.repositories.abstractions.auditable_repository import AuditableRepository


class MastYardRepository(AuditableRepository[MastYard]):
    """
    Репозиторий сущностей рей мачт
    """

    @override
    def __init__(self, session):
        super().__init__(MastYard, session)

    @override
    def _get_all_query(self, include_deleted: bool = False):
        statement = super()._get_all_query(include_deleted)
        return statement.options(selectinload(MastYard.config))

    async def get_by_height(self, config_id: UUID, height: int) -> Optional[MastYard]:
        statement = self._get_all_query().where(
            MastYard.config_id == config_id, MastYard.height == height
        )
        result = await self.session.exec(statement)
        return result.one_or_none()

    async def get_by_config(
        self, config_id: UUID, include_deleted: bool = False
    ) -> List[MastYard]:
        statement = self._get_all_query(include_deleted).where(
            MastYard.config_id == config_id
        )
        result = await self.session.exec(statement)
        return result.all()
