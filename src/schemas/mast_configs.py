from typing import List, Optional

from src.schemas.base import AuditableModelSchema, BaseSchema
from src.schemas.mast_yards import MastYardSchema


class MastConfigBaseSchema(BaseSchema):
    name: str
    height: int


class CreateMastConfigSchema(MastConfigBaseSchema):
    pass


class UpdateMastConfigSchema(MastConfigBaseSchema):
    name: Optional[str] = None
    height: Optional[int] = None


class MastConfigSchema(AuditableModelSchema, MastConfigBaseSchema):
    yards: List["MastYardSchema"]
