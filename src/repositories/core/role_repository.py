from typing import Optional, override

from sqlalchemy import func
from sqlalchemy.orm import selectinload

from src.models import Role
from src.repositories.abstractions.auditable_repository import AuditableRepository


class RoleRepository(AuditableRepository[Role]):
    """
    Репозиторий сущностей ролей
    """

    @override
    def __init__(self, session):
        super().__init__(Role, session)

    @override
    def _get_all_query(self, include_deleted: bool = False):
        statement = super()._get_all_query(include_deleted)
        return statement.options(
            selectinload(Role.parent),
            selectinload(Role.children),
            selectinload(Role.users),
            selectinload(Role.permissions),
        )

    async def get_by_name(self, name: str) -> Optional[Role]:
        statement = self._get_all_query().where(func.lower(Role.name) == name.lower())
        result = await self.session.exec(statement)
        return result.one_or_none()
