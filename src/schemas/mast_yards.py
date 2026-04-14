from typing import Optional
from uuid import UUID

from src.schemas.base import AuditableModelSchema, BaseSchema


class MastYardBaseSchema(BaseSchema):
    height: int
    amount: int


class CreateMastYardSchema(MastYardBaseSchema):
    config_id: UUID


class UpdateMastYardSchema(MastYardBaseSchema):
    height: Optional[int] = None
    amount: Optional[int] = None


class MastYardSchema(AuditableModelSchema, CreateMastYardSchema):
    pass
