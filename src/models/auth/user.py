from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from sqlmodel import Field, Relationship

from src.models.base.auditable_model import AuditableModel

if TYPE_CHECKING:
    from src.models.auth.role import Role
    from src.models.auth.role_permission import RolePermission
    from src.models.complexes.complex import Complex
    from src.models.measures.measure import Measure
from src.models.complexes.complex_access import ComplexAccess
from src.models.complexes.complex_favorite import ComplexFavorite


class User(AuditableModel, table=True):
    __tablename__ = "users"

    lastname: str = Field(nullable=False)
    firstname: str = Field(nullable=False)
    secondname: Optional[str] = Field(nullable=True)
    login: str = Field(nullable=False, unique=True, index=True)
    password_hash: str = Field(nullable=False)
    role_id: UUID = Field(foreign_key="roles.id")

    role: "Role" = Relationship(back_populates="users")
    created_role_permission_links: List["RolePermission"] = Relationship(
        back_populates="creator"
    )

    accessible_complexes: List["Complex"] = Relationship(
        back_populates="users_with_access",
        link_model=ComplexAccess,
        sa_relationship_kwargs={
            "primaryjoin": "User.id == ComplexAccess.user_id",
            "secondaryjoin": "Complex.id == ComplexAccess.complex_id",
            "overlaps": "user,complex",
        },
    )
    favorite_complexes: List["Complex"] = Relationship(
        back_populates="users_with_favorite",
        link_model=ComplexFavorite,
        sa_relationship_kwargs={
            "primaryjoin": "User.id == ComplexFavorite.user_id",
            "secondaryjoin": "Complex.id == ComplexFavorite.complex_id",
            "overlaps": "user,complex",
        },
    )
    created_complexes: List["Complex"] = Relationship(back_populates="creator")

    access_links: List["ComplexAccess"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "foreign_keys": "[ComplexAccess.user_id]",
            "cascade": "all, delete-orphan",
            "overlaps": "accessible_complexes",
        },
    )
    favorite_links: List["ComplexFavorite"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "foreign_keys": "[ComplexFavorite.user_id]",
            "cascade": "all, delete-orphan",
            "overlaps": "favorite_complexes",
        },
    )
    created_complex_access_links: List["ComplexAccess"] = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={
            "foreign_keys": "[ComplexAccess.creator_id]",
            "cascade": "all, delete-orphan",
        },
    )
    created_complex_favorite_links: List["ComplexFavorite"] = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={
            "foreign_keys": "[ComplexFavorite.creator_id]",
            "cascade": "all, delete-orphan",
        },
    )

    created_measures: List["Measure"] = Relationship(back_populates="creator")
