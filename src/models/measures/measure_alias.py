from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship

from src.models.base.auditable_model import AuditableModel

if TYPE_CHECKING:
    from src.models.measures.measure import Measure


class MeasureAlias(AuditableModel, table=True):
    __tablename__ = "measure_aliases"

    measure_id: UUID = Field(foreign_key="measures.id")
    name: str = Field(nullable=False, index=True)

    measure: "Measure" = Relationship(back_populates="aliases")
