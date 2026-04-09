from typing import TYPE_CHECKING, List

from sqlalchemy import Column, SmallInteger
from sqlmodel import Field, Relationship

from src.models.base.auditable_model import AuditableModel

if TYPE_CHECKING:
    from src.models.complexes.mast import Mast
    from src.models.complexes.mast_yard import MastYard


class MastConfig(AuditableModel, table=True):
    __tablename__ = "mast_configs"

    name: str = Field(nullable=False)
    height: int = Field(sa_column=Column(SmallInteger))

    yards: List["MastYard"] = Relationship(back_populates="config")
    masts: List["Mast"] = Relationship(back_populates="config")
