from typing import Optional, override

from sqlalchemy import func
from sqlalchemy.orm import selectinload

from src.models import Permission
from src.repositories.abstractions.auditable_repository import AuditableRepository


class PermissionRepository(AuditableRepository[Permission]):
    """
    Репозиторий сущностей разрешений
    """

    @override
    def __init__(self, session):
        super().__init__(Permission, session)

    @override
    def _get_all_query(self, include_deleted: bool = False):
        statement = super()._get_all_query(include_deleted)
        return statement.options(
            selectinload(Permission.roles),
        )

    async def get_by_name(
            self, name: str, include_deleted: bool = False) -> Optional[Permission]:
        statement = self._get_all_query(include_deleted).where(
            func.lower(Permission.name) == name.lower())
        result = await self.session.exec(statement)
        return result.one_or_none()