from typing import Optional

from src.schemas.base import ManyToManyModelSchema
from src.schemas.complexes import ComplexWithMastsSchema
from src.schemas.users import UserSchema


class ComplexAccessSchema(ManyToManyModelSchema):
    complex: ComplexWithMastsSchema
    user: UserSchema
    creator: Optional[UserSchema]
