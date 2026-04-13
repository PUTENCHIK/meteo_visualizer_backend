from typing import Dict, List, Optional, override
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import selectinload
from sqlmodel import select

from src.models import Permission, Role, RolePermission
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

    async def get_by_name(
        self, name: str, include_deleted: bool = False
    ) -> Optional[Role]:
        statement = self._get_all_query(include_deleted).where(
            func.lower(Role.name) == name.lower()
        )
        result = await self.session.exec(statement)
        return result.one_or_none()

    async def get_role_permissions(self, role_id: UUID) -> List[Permission]:
        base_query = (
            select(Role)
            .where(Role.id == role_id)
            .cte(name="role_hierarchy", recursive=True)
        )

        recursive_part = select(Role).join(
            base_query, Role.id == base_query.c.parent_id
        )

        role_hierarchy = base_query.union_all(recursive_part)

        final_query = (
            select(Permission)
            .join(RolePermission, Permission.id == RolePermission.permission_id)
            .join(role_hierarchy, RolePermission.role_id == role_hierarchy.c.id)
            .distinct()
        )
        result = await self.session.exec(final_query)
        return result.all()

    async def get_all_with_permissions(
        self, include_deleted: bool = False
    ) -> Dict[UUID, List[Permission]]:
        base_query = select(Role.id.label("root_role_id"), Role.id, Role.parent_id)

        if include_deleted:
            base_query = base_query.where(Role.deleted_at.is_(None))

        base_query = base_query.cte(name="hierarchy", recursive=True)

        recursive_part = select(
            base_query.c.root_role_id, Role.id, Role.parent_id
        ).join(base_query, Role.id == base_query.c.parent_id)

        hierarchy_cte = base_query.union_all(recursive_part)

        stmt = (
            select(hierarchy_cte.c.root_role_id, Permission)
            .join(RolePermission, hierarchy_cte.c.id == RolePermission.role_id)
            .join(Permission, RolePermission.permission_id == Permission.id)
            .distinct()
        )

        result = await self.session.exec(stmt)

        grouped_perms: Dict[UUID, List[Permission]] = dict()
        for root_id, perm in result.all():
            if root_id not in grouped_perms:
                grouped_perms[root_id] = []
            grouped_perms[root_id].append(perm)

        return grouped_perms
