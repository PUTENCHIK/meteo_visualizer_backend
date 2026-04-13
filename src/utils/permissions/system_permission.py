from enum import Enum


class SystemPermission(Enum):
    USER_READ = "user:read"
    USER_CREATE = "user:create"
    ROLE_READ = "role:read"
    ROLE_CREATE = "role:create"
    ROLE_UPDATE = "role:update"
    ROLE_DELETE = "role:delete"
    PERMISSION_UPDATE = "permission:update"
