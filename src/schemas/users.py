from typing import List, Optional
from uuid import UUID

from src.schemas.base import AuditableModelSchema, BaseSchema
from src.schemas.complexes import ComplexBaseSchema
from src.schemas.roles import RoleSchema, RoleWithPermissionsSchema


class NamesSchema(BaseSchema):
    lastname: str
    firstname: str
    secondname: str


class LoginSchema(BaseSchema):
    login: str


class PasswordSchema(BaseSchema):
    password: str


class RoleIdSchema(BaseSchema):
    role_id: UUID


class UserBaseSchema(NamesSchema, LoginSchema, RoleIdSchema):
    pass


class UpdateUserSchema(NamesSchema, RoleIdSchema):
    lastname: Optional[str] = None
    firstname: Optional[str] = None
    secondname: Optional[str] = None
    role_id: Optional[UUID] = None


class UserSchema(AuditableModelSchema, UserBaseSchema):
    role: RoleSchema


class ActiveUserSchema(UserSchema):
    role: RoleWithPermissionsSchema
    complexes: List["ComplexBaseSchema"]
    created_complexes: List["ComplexBaseSchema"]
