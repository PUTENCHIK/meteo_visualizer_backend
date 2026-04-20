from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from src.schemas.base import AuditableModelSchema, BaseSchema
from src.schemas.roles import RoleSchema, RoleWithPermissionsSchema

if TYPE_CHECKING:
    from src.schemas.complexes import ComplexSchema


class NamesSchema(BaseSchema):
    lastname: str
    firstname: str
    secondname: Optional[str] = None


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
    role_id: Optional[UUID] = None


class UserSchema(AuditableModelSchema, UserBaseSchema):
    pass


class UserWithRoleSchema(UserSchema):
    role: RoleSchema


class ActiveUserSchema(UserWithRoleSchema):
    role: RoleWithPermissionsSchema
    accessible_complexes: List["ComplexSchema"]
    favorite_complexes: List["ComplexSchema"]
    created_complexes: List["ComplexSchema"]
