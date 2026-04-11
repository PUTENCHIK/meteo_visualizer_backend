from typing import List, Optional
from uuid import UUID

from src.schemas.auth import UserSchema
from src.schemas.base import AuditableModelSchema, BaseSchema


class RoleBaseSchema(BaseSchema):
    name: str
    parent_id: Optional[UUID]


class CreateRoleSchema(RoleBaseSchema):
    pass


class UpdateRoleSchema(RoleBaseSchema):
    name: Optional[str] = None
    parent_id: Optional[UUID] = None


class RoleSchema(AuditableModelSchema, RoleBaseSchema):
    pass


class RoleWithParentSchema(RoleSchema):
    parent: Optional["RoleSchema"]
    children: List["RoleSchema"]


class RoleWithUsersSchema(RoleWithParentSchema):
    users: List["UserSchema"]
