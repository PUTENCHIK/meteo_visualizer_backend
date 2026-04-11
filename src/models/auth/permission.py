from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship

from src.models.auth.role_permission import RolePermission
from src.models.base.auditable_model import AuditableModel

if TYPE_CHECKING:
    from src.models.auth.role import Role


class Permission(AuditableModel, table=True):
    __tablename__ = "permissions"

    name: str = Field(unique=True, index=True, nullable=False)
    description: str = Field(nullable=False)

    roles: List["Role"] = Relationship(
        back_populates="permissions",
        link_model=RolePermission,
        sa_relationship_kwargs={"overlaps": "role,permission"},
    )
