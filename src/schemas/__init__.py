from src.schemas.auth import (
    AuthTokensSchema as AuthTokensSchema,
    SigninSchema as SigninSchema,
    SignupSchema as SignupSchema,
    UserSchema as UserSchema,
)
from src.schemas.responses import (
    ErrorResponse as ErrorResponse,
    ResponseModel as ResponseModel,
)
from src.schemas.roles import (
    CreateRoleSchema as CreateRoleSchema,
    UpdateRoleSchema as UpdateRoleSchema,
    RoleBaseSchema as RoleBaseSchema,
    RoleSchema as RoleSchema,
    RoleWithParentSchema as RoleWithParentSchema,
    RoleWithPermissionsSchema as RoleWithPermissionsSchema,
)
from src.schemas.permissions import (
    CreatePermissionSchema as CreatePermissionSchema,
    UpdatePermissionSchema as UpdatePermissionSchema,
    PermissionSchema as PermissionSchema,
    PermissionWithRolesSchema as PermissionWithRolesSchema,
)
from src.schemas.roles_permissions import (
    AddPermissionToRoleSchema as AddPermissionToRoleSchema,
    DeletePermissionToRoleSchema as DeletePermissionToRoleSchema,
    CreateRolePermissionSchema as CreateRolePermissionSchema,
    RolePermissionSchema as RolePermissionSchema,
)

RoleWithPermissionsSchema.model_rebuild()
PermissionWithRolesSchema.model_rebuild()