from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, Numeric
from sqlmodel import Field, Relationship

from src.models.base.auditable_model import AuditableModel

if TYPE_CHECKING:
    from src.models.complexes.complex import Complex
    from src.models.complexes.mast_config import MastConfig


class Mast(AuditableModel, table=True):
    __tablename__ = "masts"

    complex_id: UUID = Field(foreign_key="complexes.id")
    config_id: UUID = Field(foreign_key="mast_configs.id")
    latitude: Decimal = Field(sa_column=Column(Numeric(precision=8, scale=6)))
    longitude: Decimal = Field(sa_column=Column(Numeric(precision=9, scale=6)))

    complex: "Complex" = Relationship(back_populates="masts")
    config: "MastConfig" = Relationship(back_populates="masts")
