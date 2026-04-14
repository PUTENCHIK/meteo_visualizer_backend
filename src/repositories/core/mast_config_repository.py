from typing import override

from sqlalchemy.orm import selectinload

from src.models import Mast, MastConfig, MastYard
from src.repositories.abstractions.auditable_repository import AuditableRepository


class MastConfigRepository(AuditableRepository[MastConfig]):
    """
    Репозиторий сущностей конфигов мачт
    """

    @override
    def __init__(self, session):
        super().__init__(MastConfig, session)

    @override
    def _get_all_query(self, include_deleted: bool = False):
        statement = super()._get_all_query(include_deleted)
        return statement.options(
            selectinload(MastConfig.yards.and_(MastYard.deleted_at is None)),
            selectinload(MastConfig.masts.and_(Mast.deleted_at is None)),
        )
