from typing import Optional
from uuid import UUID

from src.schemas.base import ManyToManyModelSchema
from src.schemas.complexes import ComplexSchema
from src.schemas.users import UserSchema


class ComplexAccessSchema(ManyToManyModelSchema):
    complex_id: UUID
    complex: ComplexSchema
    user_id: UUID
    user: UserSchema
    creator: Optional[UserSchema]
