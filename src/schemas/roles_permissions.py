from typing import Optional
from uuid import UUID

from src.auth.enums import SystemPermission
from src.schemas.base import BaseSchema, ManyToManyModelSchema
from src.schemas.permissions import PermissionSchema
from src.schemas.roles import RoleSchema
from src.schemas.users import UserWithRoleSchema


class AddPermissionToRoleSchema(BaseSchema):
    permission: SystemPermission


class DeletePermissionFromRoleSchema(AddPermissionToRoleSchema):
    pass


class CreateRolePermissionSchema(AddPermissionToRoleSchema):
    role_id: UUID


class RolePermissionSchema(ManyToManyModelSchema):
    role: RoleSchema
    permission: PermissionSchema
    creator: Optional[UserWithRoleSchema]
