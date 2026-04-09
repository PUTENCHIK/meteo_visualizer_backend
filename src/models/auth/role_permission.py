from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlmodel import Field, Relationship

from src.models.base.many_to_many_model import ManyToManyModel

if TYPE_CHECKING:
    from src.models.auth.permission import Permission
    from src.models.auth.role import Role
    from src.models.auth.user import User


class RolePermission(ManyToManyModel, table=True):
    __tablename__ = "roles_permissions"

    role_id: UUID = Field(foreign_key="roles.id", primary_key=True)
    permission_id: UUID = Field(foreign_key="permissions.id", primary_key=True)
    creator_id: Optional[UUID] = Field(foreign_key="users.id", default=None)

    role: "Role" = Relationship(back_populates="permissions")
    permission: "Permission" = Relationship(back_populates="roles")
    creator: Optional["User"] = Relationship(
        back_populates="created_role_permission_links"
    )
