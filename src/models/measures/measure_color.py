from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, Numeric
from sqlmodel import Field, Relationship

from src.models.base.auditable_model import AuditableModel

if TYPE_CHECKING:
    from src.models.measures.measure import Measure


class MeasureColor(AuditableModel, table=True):
    __tablename__ = "measure_colors"

    measure_id: UUID = Field(foreign_key="measures.id")
    value: str = Field(nullable=False, max_length=6)
    percent: Decimal = Field(sa_column=Column(Numeric(precision=3, scale=2)))

    measure: "Measure" = Relationship(back_populates="colors")
