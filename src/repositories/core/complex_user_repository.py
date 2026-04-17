from typing import List, Optional, override
from uuid import UUID

from sqlalchemy.orm import selectinload

from src.models import ComplexUser
from src.repositories.abstractions.many_to_many_repository import ManyToManyRepository


class ComplexUserRepository(ManyToManyRepository[ComplexUser]):
    """
    Репозиторий сущностей связей между комплексами и пользователями
    """

    @override
    def __init__(self, session):
        super().__init__(ComplexUser, session)

    @override
    def _get_all_query(self):
        statement = super()._get_all_query()
        return statement.options(
            selectinload(ComplexUser.complex),
            selectinload(ComplexUser.user),
            selectinload(ComplexUser.creator),
        )

    @override
    async def get_by_ids(
        self, complex_id: UUID, user_id: UUID
    ) -> Optional[ComplexUser]:
        statement = self._get_all_query().where(
            ComplexUser.complex_id == complex_id,
            ComplexUser.user_id == user_id,
        )
        result = await self.session.exec(statement)
        return result.one_or_none()

    async def get_by_user(self, user_id: UUID) -> List[ComplexUser]:
        statement = super()._get_all_query().where(ComplexUser.user_id == user_id)
        result = await self.session.exec(statement)
        return result.all()
