from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from src.schemas.base import AuditableModelSchema, BaseSchema
from src.schemas.measure_aliases import MeasureAliasSchema
from src.schemas.measure_colors import MeasureColorSchema

if TYPE_CHECKING:
    from src.schemas.users import UserWithRoleSchema


class CreatorIdSchema(BaseSchema):
    creator_id: Optional[UUID] = None


class MeasureBaseSchema(BaseSchema):
    name: str
    min: int
    max: int
    units: str


class CreateMeasureSchema(MeasureBaseSchema):
    pass


class UpdateMeasureSchema(CreateMeasureSchema):
    name: Optional[str] = None
    min: Optional[int] = None
    max: Optional[int] = None
    units: Optional[str] = None


class MeasureSchema(AuditableModelSchema, MeasureBaseSchema, CreatorIdSchema):
    pass


class MeasureWithCreatorSchema(MeasureSchema):
    creator: Optional["UserWithRoleSchema"] = None


class MeasureWithDependentsSchema(MeasureWithCreatorSchema):
    colors: List[MeasureColorSchema]
    aliases: List[MeasureAliasSchema]
