from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from sqlalchemy import Column, Numeric
from sqlmodel import Field, Relationship

from src.models.base.auditable_model import AuditableModel

if TYPE_CHECKING:
    from src.models.auth.user import User
    from src.models.complexes.mast import Mast
from src.models.complexes.complex_user import ComplexUser


class Complex(AuditableModel, table=True):
    __tablename__ = "complexes"

    name: str = Field(nullable=False, index=True)
    creator_id: UUID = Field(foreign_key="users.id")
    password_hash: Optional[str] = Field(default=None)
    is_private: bool = Field(default=False, index=True)
    latitude: Decimal = Field(sa_column=Column(Numeric(precision=8, scale=6)))
    longitude: Decimal = Field(sa_column=Column(Numeric(precision=9, scale=6)))
    address: Optional[str] = Field(default=None)

    creator: "User" = Relationship(back_populates="created_complexes")
    masts: List["Mast"] = Relationship(back_populates="complex")
    users: List["User"] = Relationship(
        back_populates="complexes", link_model=ComplexUser
    )
