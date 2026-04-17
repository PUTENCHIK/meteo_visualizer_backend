from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from sqlmodel import Field, Relationship

from src.models.base.auditable_model import AuditableModel

if TYPE_CHECKING:
    from src.models.auth.user import User
    from src.models.measures.measure_alias import MeasureAlias
    from src.models.measures.measure_color import MeasureColor


class Measure(AuditableModel, table=True):
    __tablename__ = "measures"

    creator_id: Optional[UUID] = Field(foreign_key="users.id", nullable=True)
    name: str = Field(nullable=False)
    min: int = Field()
    max: int = Field()
    units: Optional[str] = Field(nullable=True, default=None)

    creator: Optional["User"] = Relationship(back_populates="created_measures")
    aliases: List["MeasureAlias"] = Relationship(back_populates="measure")
    colors: List["MeasureColor"] = Relationship(back_populates="measure")
