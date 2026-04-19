from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from src.schemas.base import AuditableModelSchema, BaseSchema
from src.schemas.masts import MastSchema

if TYPE_CHECKING:
    from src.schemas.users import UserSchema


class SecretkeySchema(BaseSchema):
    secretkey: Optional[str] = None


class ComplexBaseSchema(BaseSchema):
    name: str
    is_private: bool
    latitude: Decimal
    longitude: Decimal
    address: Optional[str] = None


class CreateComplexSchema(ComplexBaseSchema, SecretkeySchema):
    pass


class UpdateComplexSchema(ComplexBaseSchema, SecretkeySchema):
    name: Optional[str] = None
    is_private: Optional[bool] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None


class ComplexSchema(AuditableModelSchema, ComplexBaseSchema):
    creator_id: UUID
    creator: "UserSchema"
    is_secreted: bool


class ComplexWithMastsSchema(ComplexSchema):
    masts: List[MastSchema]


class ComplexFullSchema(ComplexWithMastsSchema):
    secretkey: Optional[str]
