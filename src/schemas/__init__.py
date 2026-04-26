from src.schemas.auth import (
    AuthTokensSchema as AuthTokensSchema,
    SigninSchema as SigninSchema,
    SignupSchema as SignupSchema,
)
from src.schemas.complex_accesses import (
    ComplexAccessSchema as ComplexAccessSchema,
)
from src.schemas.complex_favorites import ComplexFavoriteSchema as ComplexFavoriteSchema
from src.schemas.complexes import (
    ComplexSchema as ComplexSchema,
    ComplexWithCreatorSchema as ComplexWithCreatorSchema,
    ComplexWithFavoriteInfoSchema as ComplexWithFavoriteInfoSchema,
    ComplexWithMastsSchema as ComplexWithMastsSchema,
    CreateComplexSchema as CreateComplexSchema,
    UpdateComplexSchema as UpdateComplexSchema,
)
from src.schemas.mast_configs import (
    CreateMastConfigSchema as CreateMastConfigSchema,
    MastConfigSchema as MastConfigSchema,
    UpdateMastConfigSchema as UpdateMastConfigSchema,
)
from src.schemas.mast_yards import (
    CreateMastYardSchema as CreateMastYardSchema,
    MastYardSchema as MastYardSchema,
    UpdateMastYardSchema as UpdateMastYardSchema,
)
from src.schemas.masts import (
    CreateMastSchema as CreateMastSchema,
    MastSchema as MastSchema,
    UpdateMastSchema as UpdateMastSchema,
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
    DeletePermissionFromRoleSchema as DeletePermissionFromRoleSchema,
    RolePermissionSchema as RolePermissionSchema,
)
from src.schemas.users import (
    ActiveUserSchema as ActiveUserSchema,
    UserWithComplexesSchema as UserWithComplexesSchema,
    UpdateUserSchema as UpdateUserSchema,
    UserSchema as UserSchema,
    UserWithRoleSchema as UserWithRoleSchema,
)

RoleWithPermissionsSchema.model_rebuild()
PermissionWithRolesSchema.model_rebuild()
ComplexWithCreatorSchema.model_rebuild()
ComplexWithMastsSchema.model_rebuild()
ComplexWithFavoriteInfoSchema.model_rebuild()
UserWithComplexesSchema.model_rebuild()
ActiveUserSchema.model_rebuild()
