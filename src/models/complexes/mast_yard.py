from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Column, SmallInteger
from sqlmodel import Field, Relationship

from src.models.base.auditable_model import AuditableModel

if TYPE_CHECKING:
    from src.models.complexes.mast_config import MastConfig


class MastYard(AuditableModel, table=True):
    __tablename__ = "mast_yards"

    config_id: UUID = Field(foreign_key="mast_configs.id")
    height: int = Field(sa_column=Column(SmallInteger))
    amount: int = Field(sa_column=Column(SmallInteger))

    config: "MastConfig" = Relationship(back_populates="yards")
