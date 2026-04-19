from typing import List, Optional, override
from uuid import UUID

from sqlalchemy.orm import selectinload

from src.models import ComplexAccess
from src.repositories.abstractions.many_to_many_repository import ManyToManyRepository


class ComplexAccessRepository(ManyToManyRepository[ComplexAccess]):
    """
    Репозиторий сущностей доступов пользователей к комплексам
    """

    @override
    def __init__(self, session):
        super().__init__(ComplexAccess, session)

    @override
    def _get_all_query(self):
        statement = super()._get_all_query()
        return statement.options(
            selectinload(ComplexAccess.complex),
            selectinload(ComplexAccess.user),
            selectinload(ComplexAccess.creator),
        )

    @override
    async def get_by_ids(
        self, complex_id: UUID, user_id: UUID
    ) -> Optional[ComplexAccess]:
        statement = self._get_all_query().where(
            ComplexAccess.complex_id == complex_id,
            ComplexAccess.user_id == user_id,
        )
        result = await self.session.exec(statement)
        return result.one_or_none()

    async def get_by_user(self, user_id: UUID) -> List[ComplexAccess]:
        statement = super()._get_all_query().where(ComplexAccess.user_id == user_id)
        result = await self.session.exec(statement)
        return result.all()
