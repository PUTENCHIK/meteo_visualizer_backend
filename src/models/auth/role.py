from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from sqlmodel import Field, Relationship

from src.models.base.auditable_model import AuditableModel

if TYPE_CHECKING:
    from src.models.auth.permission import Permission
    from src.models.auth.user import User
from src.models.auth.role_permission import RolePermission


class Role(AuditableModel, table=True):
    __tablename__ = "roles"

    name: str = Field(unique=True, index=True)
    parent_id: Optional[UUID] = Field(foreign_key="roles.id")

    parent: Optional["Role"] = Relationship(
        back_populates="children", sa_relationship_kwargs={"remote_side": "Role.id"}
    )
    children: List["Role"] = Relationship(back_populates="parent")
    users: List["User"] = Relationship(back_populates="role")
    permissions: List["Permission"] = Relationship(
        back_populates="roles", link_model=RolePermission
    )
