from typing import override

from sqlalchemy.orm import selectinload

from src.models import Complex, Mast, MastConfig, MastYard, User
from src.repositories.abstractions.auditable_repository import AuditableRepository


class ComplexRepository(AuditableRepository[Complex]):
    """
    Репозиторий сущностей комплексов
    """

    @override
    def __init__(self, session):
        super().__init__(Complex, session)

    @override
    def _get_all_query(self, include_deleted: bool = False):
        statement = super()._get_all_query(include_deleted)
        return statement.options(
            selectinload(Complex.creator).selectinload(User.role),
            (
                selectinload(Complex.masts.and_(Mast.deleted_at.is_(None)))
                .selectinload(Mast.config)
                .selectinload(MastConfig.yards.and_(MastYard.deleted_at.is_(None)))
            ),
            selectinload(
                Complex.users_with_access.and_(User.deleted_at.is_(None))
            ).selectinload(User.role),
            selectinload(
                Complex.users_with_favorite.and_(User.deleted_at.is_(None))
            ).selectinload(User.role),
        )
