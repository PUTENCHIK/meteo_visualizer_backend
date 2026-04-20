from enum import Enum


class SystemPermission(Enum):
    ROLE_READ = "role:read"
    ROLE_CREATE = "role:create"
    ROLE_RESTORE = "role:restore"
    ROLE_UPDATE = "role:update"
    ROLE_DELETE = "role:delete"

    ROLE_PERMISSION_CREATE = "role_permission:create"
    ROLE_PERMISSION_DELETE = "role_permission:delete"

    PERMISSION_READ = "permission:read"
    PERMISSION_UPDATE = "permission:update"

    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_RESTORE = "user:restore"
    USER_DELETE = "user:delete"

    COMPLEX_READ = "complex:read"
    COMPLEX_CREATE = "complex:create"
    COMPLEX_RESTORE = "complex:restore"
    COMPLEX_UPDATE = "complex:update"
    COMPLEX_DELETE = "complex:delete"

    MAST_READ = "mast:read"
    MAST_CREATE = "mast:create"
    MAST_UPDATE = "mast:update"
    MAST_DELETE = "mast:delete"

    MAST_CONFIG_READ = "mast_config:read"
    MAST_CONFIG_CREATE = "mast_config:create"
    MAST_CONFIG_RESTORE = "mast_config:restore"
    MAST_CONFIG_UPDATE = "mast_config:update"
    MAST_CONFIG_DELETE = "mast_config:delete"

    MAST_YARD_READ = "mast_yard:read"
    MAST_YARD_CREATE = "mast_yard:create"
    MAST_YARD_UPDATE = "mast_yard:update"
    MAST_YARD_DELETE = "mast_yard:delete"

    COMPLEX_FAVORITE_CREATE = "complex_favorite:create"
    COMPLEX_FAVORITE_DELETE = "complex_favorite:delete"
