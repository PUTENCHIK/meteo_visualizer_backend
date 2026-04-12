from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)


class BaseModelSchema(BaseSchema):
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UuidModel(BaseSchema):
    id: UUID


class AuditableModelSchema(UuidModel, BaseModelSchema):
    updated_at: datetime
    deleted_at: Optional[datetime]


class ManyToManyModelSchema(BaseModelSchema):
    creator_id: Optional[UUID]
