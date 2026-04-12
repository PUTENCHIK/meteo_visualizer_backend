from typing import List, Optional, TYPE_CHECKING
from src.schemas.base import AuditableModelSchema, BaseSchema

if TYPE_CHECKING:
    from src.schemas.roles import RoleWithParentSchema


class PermissionBaseSchema(BaseSchema):
    name: str
    description: str

class CreatePermissionSchema(PermissionBaseSchema):
    pass


class UpdatePermissionSchema(BaseSchema):
    description: Optional[str] = None


class PermissionSchema(AuditableModelSchema, PermissionBaseSchema):
    pass


class PermissionWithRolesSchema(PermissionSchema):
    roles: List["RoleWithParentSchema"]
