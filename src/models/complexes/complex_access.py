from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlmodel import Field, Relationship

from src.models.base.many_to_many_model import ManyToManyModel

if TYPE_CHECKING:
    from src.models.auth.user import User
    from src.models.complexes.complex import Complex


class ComplexAccess(ManyToManyModel, table=True):
    __tablename__ = "complex_accesses"

    complex_id: UUID = Field(foreign_key="complexes.id", primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", primary_key=True)
    creator_id: Optional[UUID] = Field(foreign_key="users.id", default=None)

    complex: "Complex" = Relationship()
    user: "User" = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[ComplexAccess.user_id]"}
    )
    creator: Optional["User"] = Relationship(
        back_populates="created_complex_access_links",
        sa_relationship_kwargs={"foreign_keys": "[ComplexAccess.creator_id]"},
    )
