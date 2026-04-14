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
