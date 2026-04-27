from typing import Optional
from uuid import UUID

from src.schemas.base import AuditableModelSchema, BaseSchema


class MeasureIdSchema(BaseSchema):
    measure_id: UUID


class MeasureAliasBaseSchema(BaseSchema):
    name: str


class CreateMeasureAliasSchema(MeasureIdSchema, MeasureAliasBaseSchema):
    pass


class UpdateMeasureAliasSchema(MeasureAliasBaseSchema):
    name: Optional[str] = None


class MeasureAliasSchema(AuditableModelSchema, CreateMeasureAliasSchema):
    pass
