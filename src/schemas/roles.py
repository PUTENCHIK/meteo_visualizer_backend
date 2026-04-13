from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from src.schemas.base import AuditableModelSchema, BaseSchema, UuidModel

if TYPE_CHECKING:
    from src.schemas.permissions import PermissionSchema


class RoleBaseSchema(BaseSchema):
    name: str
    parent_id: Optional[UUID] = None


class CreateRoleSchema(UuidModel, RoleBaseSchema):
    id: Optional[UUID] = None


class UpdateRoleSchema(RoleBaseSchema):
    name: Optional[str] = None
    parent_id: Optional[UUID] = None


class RoleSchema(AuditableModelSchema, RoleBaseSchema):
    pass


class RoleWithParentSchema(RoleSchema):
    parent: Optional["RoleSchema"]
    children: List["RoleSchema"]


class RoleWithPermissionsSchema(RoleWithParentSchema):
    permissions: List["PermissionSchema"]
