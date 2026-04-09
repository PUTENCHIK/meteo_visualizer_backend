from typing import TYPE_CHECKING, List
from uuid import UUID

from pydantic import computed_field
from sqlmodel import Field, Relationship

from src.models.base.auditable_model import AuditableModel

if TYPE_CHECKING:
    from src.models.auth.permission import Permission
    from src.models.auth.role import Role
    from src.models.auth.role_permission import RolePermission
    from src.models.complexes.complex import Complex
    from src.models.measures.measure import Measure
from src.models.complexes.complex_user import ComplexUser


class User(AuditableModel, table=True):
    __tablename__ = "users"

    lastname: str = Field(nullable=False)
    firstname: str = Field(nullable=False)
    secondname: str = Field(nullable=False)
    login: str = Field(nullable=False, unique=True, index=True)
    password_hash: str = Field(nullable=False)
    role_id: UUID = Field(foreign_key="roles.id")

    role: "Role" = Relationship(back_populates="users")
    complexes: List["Complex"] = Relationship(
        back_populates="users", link_model=ComplexUser
    )
    created_complexes: List["Complex"] = Relationship(back_populates="creator")
    created_role_permission_links: List["RolePermission"] = Relationship(
        back_populates="creator"
    )
    created_complex_user_links: List["ComplexUser"] = Relationship(
        back_populates="creator"
    )
    measures: List["Measure"] = Relationship(back_populates="user")

    @property
    @computed_field
    def permissions(self) -> List["Permission"]:
        if not self.role:
            return []

        permissions = set()
        role = self.role

        while role is not None:
            permissions.update(role.permissions)
            role = role.parent

        return list(permissions)
