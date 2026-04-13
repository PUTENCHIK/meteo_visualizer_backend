from uuid import UUID

from src.schemas.base import BaseSchema
from src.schemas.permissions import PermissionSchema
from src.schemas.roles import RoleSchema
from src.utils.permissions import SystemPermission


class AddPermissionToRoleSchema(BaseSchema):
    permission: SystemPermission


class DeletePermissionToRoleSchema(AddPermissionToRoleSchema):
    pass


class CreateRolePermissionSchema(AddPermissionToRoleSchema):
    role_id: UUID


class RolePermissionSchema(BaseSchema):
    role: RoleSchema
    permission: PermissionSchema
