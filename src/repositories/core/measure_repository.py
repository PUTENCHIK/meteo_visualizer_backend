from typing import override

from sqlalchemy.orm import selectinload

from src.models import Measure, User
from src.repositories.abstractions.auditable_repository import AuditableRepository


class MeasureRepository(AuditableRepository[Measure]):
    """
    Репозиторий сущностей пользовательских параметров визуализации
    """

    @override
    def __init__(self, session):
        super().__init__(Measure, session)

    @override
    def _get_all_query(self, include_deleted: bool = False):
        statement = super()._get_all_query(include_deleted)
        return statement.options(
            selectinload(Measure.colors),
            selectinload(Measure.aliases),
            selectinload(Measure.creator).selectinload(User.role),
        )
