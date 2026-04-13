from src.schemas.auth import (
    AuthTokensSchema as AuthTokensSchema,
    RefreshTokenSchema as RefreshTokenSchema,
    SigninSchema as SigninSchema,
    SignupSchema as SignupSchema,
)
from src.schemas.permissions import (
    CreatePermissionSchema as CreatePermissionSchema,
    PermissionSchema as PermissionSchema,
    PermissionWithRolesSchema as PermissionWithRolesSchema,
    UpdatePermissionSchema as UpdatePermissionSchema,
)
from src.schemas.responses import (
    ErrorResponse as ErrorResponse,
    ResponseModel as ResponseModel,
)
from src.schemas.roles import (
    CreateRoleSchema as CreateRoleSchema,
    RoleBaseSchema as RoleBaseSchema,
    RoleSchema as RoleSchema,
    RoleWithParentSchema as RoleWithParentSchema,
    RoleWithPermissionsSchema as RoleWithPermissionsSchema,
    UpdateRoleSchema as UpdateRoleSchema,
)
from src.schemas.roles_permissions import (
    AddPermissionToRoleSchema as AddPermissionToRoleSchema,
    CreateRolePermissionSchema as CreateRolePermissionSchema,
    DeletePermissionToRoleSchema as DeletePermissionToRoleSchema,
    RolePermissionSchema as RolePermissionSchema,
)
from src.schemas.users import (
    UpdateUserSchema as UpdateUserSchema,
    UserSchema as UserSchema,
)

RoleWithPermissionsSchema.model_rebuild()
PermissionWithRolesSchema.model_rebuild()
