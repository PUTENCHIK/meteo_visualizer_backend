from typing import List, Optional, override
from uuid import UUID

from sqlalchemy.orm import selectinload
from sqlmodel import select

from src.models import ComplexFavorite
from src.repositories.abstractions.many_to_many_repository import ManyToManyRepository


class ComplexFavoriteRepository(ManyToManyRepository[ComplexFavorite]):
    """
    Репозиторий сущностей избранных комплексов у пользователей
    """

    @override
    def __init__(self, session):
        super().__init__(ComplexFavorite, session)

    @override
    def _get_all_query(self):
        statement = super()._get_all_query()
        return statement.options(
            selectinload(ComplexFavorite.complex),
            selectinload(ComplexFavorite.user),
            selectinload(ComplexFavorite.creator),
        )

    @override
    async def get_by_ids(
        self, complex_id: UUID, user_id: UUID
    ) -> Optional[ComplexFavorite]:
        statement = self._get_all_query().where(
            ComplexFavorite.complex_id == complex_id,
            ComplexFavorite.user_id == user_id,
        )
        result = await self.session.exec(statement)
        return result.one_or_none()

    async def get_by_user(self, user_id: UUID) -> List[ComplexFavorite]:
        statement = super()._get_all_query().where(ComplexFavorite.user_id == user_id)
        result = await self.session.exec(statement)
        return result.all()

    async def get_favorites_of_user(
        self, user_id: UUID, complex_ids: List[UUID]
    ) -> List[UUID]:
        statement = select(ComplexFavorite.complex_id).where(
            ComplexFavorite.user_id == user_id,
            ComplexFavorite.complex_id.in_(complex_ids),
        )
        result = await self._session.exec(statement)
        return result.all()
