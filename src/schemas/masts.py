from decimal import Decimal
from typing import Optional
from uuid import UUID

from src.schemas.base import AuditableModelSchema, BaseSchema
from src.schemas.mast_configs import MastConfigSchema


class MastBaseSchema(BaseSchema):
    config_id: UUID
    latitude: Decimal
    longitude: Decimal


class CreateMastSchema(MastBaseSchema):
    complex_id: UUID


class UpdateMastSchema(MastBaseSchema):
    config_id: Optional[UUID] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None


class MastSchema(AuditableModelSchema, CreateMastSchema):
    config: MastConfigSchema
