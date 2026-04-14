from typing import override

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
                MastConfig.yards.and_(MastYard.deleted_at is None)
            ),
            selectinload(Mast.complex),
        )
