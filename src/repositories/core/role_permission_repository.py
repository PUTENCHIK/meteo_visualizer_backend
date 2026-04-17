from typing import List, Optional, override
from uuid import UUID

from sqlalchemy.orm import selectinload

from src.models import RolePermission
from src.repositories.abstractions.many_to_many_repository import ManyToManyRepository


class RolePermissionRepository(ManyToManyRepository[RolePermission]):
    """
    Репозиторий сущностей связей между ролями и разрешениями
    """

    @override
    def __init__(self, session):
        super().__init__(RolePermission, session)

    @override
    def _get_all_query(self):
        statement = super()._get_all_query()
        return statement.options(
            selectinload(RolePermission.role),
            selectinload(RolePermission.permission),
            selectinload(RolePermission.creator),
        )

    @override
    async def get_by_ids(
        self, role_id: UUID, permission_id: UUID
    ) -> Optional[RolePermission]:
        statement = self._get_all_query().where(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id,
        )
        result = await self.session.exec(statement)
        return result.one_or_none()

    async def get_by_role(self, role_id: UUID) -> List[RolePermission]:
        statement = super()._get_all_query().where(RolePermission.role_id == role_id)
        result = await self.session.exec(statement)
        return result.all()
