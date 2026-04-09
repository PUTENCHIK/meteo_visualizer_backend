from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlmodel import Field, Relationship

from src.models.base.many_to_many_model import ManyToManyModel

if TYPE_CHECKING:
    from src.models.auth.user import User
    from src.models.complexes.complex import Complex


class ComplexUser(ManyToManyModel, table=True):
    __tablename__ = "complexes_users"

    complex_id: UUID = Field(foreign_key="complexes.id", primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", primary_key=True)
    creator_id: Optional[UUID] = Field(foreign_key="users.id", default=None)

    complex: "Complex" = Relationship(back_populates="users")
    user: "User" = Relationship(back_populates="complexes")
    creator: Optional["User"] = Relationship(
        back_populates="created_complex_user_links"
    )
