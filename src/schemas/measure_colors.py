from typing import Optional
from uuid import UUID

from pydantic import Field

from src.schemas.base import AuditableModelSchema, BaseSchema


class MeasureIdSchema(BaseSchema):
    measure_id: UUID


class MeasureColorBaseSchema(BaseSchema):
    value: str
    percent: float


class CreateMeasureColorSchema(MeasureIdSchema, MeasureColorBaseSchema):
    value: str = Field(..., min_length=7, max_length=7)
    percent: float = Field(0, ge=0, le=1)


class UpdateMeasureColorSchema(MeasureColorBaseSchema):
    value: Optional[str] = Field(None, min_length=7, max_length=7)
    percent: Optional[float] = Field(None, ge=0, le=1)


class MeasureColorSchema(AuditableModelSchema, MeasureIdSchema, MeasureColorBaseSchema):
    pass
