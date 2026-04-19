from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from sqlalchemy import Column, Numeric
from sqlmodel import Field, Relationship

from src.models.base.auditable_model import AuditableModel

if TYPE_CHECKING:
    from src.models.auth.user import User
    from src.models.complexes.mast import Mast
from src.models.complexes.complex_access import ComplexAccess
from src.models.complexes.complex_favorite import ComplexFavorite


class Complex(AuditableModel, table=True):
    __tablename__ = "complexes"

    name: str = Field(nullable=False, index=True)
    creator_id: UUID = Field(foreign_key="users.id")
    secretkey: Optional[str] = Field(default=None)
    is_private: bool = Field(default=False, index=True)
    latitude: Decimal = Field(sa_column=Column(Numeric(precision=8, scale=6)))
    longitude: Decimal = Field(sa_column=Column(Numeric(precision=9, scale=6)))
    address: Optional[str] = Field(default=None)

    creator: "User" = Relationship(back_populates="created_complexes")
    masts: List["Mast"] = Relationship(back_populates="complex")

    users_with_access: List["User"] = Relationship(
        back_populates="accessible_complexes",
        link_model=ComplexAccess,
        sa_relationship_kwargs={
            "primaryjoin": "Complex.id == ComplexAccess.complex_id",
            "secondaryjoin": "User.id == ComplexAccess.user_id",
            "overlaps": "complex,access_links,user",
        },
    )
    users_with_favorite: List["User"] = Relationship(
        back_populates="favorite_complexes",
        link_model=ComplexFavorite,
        sa_relationship_kwargs={
            "primaryjoin": "Complex.id == ComplexFavorite.complex_id",
            "secondaryjoin": "User.id == ComplexFavorite.user_id",
            "overlaps": "complex,favorite_links,user",
        },
    )

    access_links: List["ComplexAccess"] = Relationship(
        back_populates="complex",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "overlaps": "accessible_complexes,users_with_access",
        },
    )
    favorite_links: List["ComplexFavorite"] = Relationship(
        back_populates="complex",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "overlaps": "favorite_complexes,users_with_favorite",
        },
    )

    @property
    def is_secreted(self) -> bool:
        return self.secretkey is not None
