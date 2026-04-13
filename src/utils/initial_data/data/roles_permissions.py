from uuid import UUID

from src.auth.enums import SystemPermission as value
from src.schemas import CreateRolePermissionSchema as RP

INITIAL_ROLES_PERMISSIONS = [
    RP(role_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"), permission=value.ROLE_READ),
    RP(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=value.ROLE_CREATE),
    RP(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=value.ROLE_RESTORE),
    RP(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=value.ROLE_UPDATE),
    RP(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=value.ROLE_DELETE),
    RP(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=value.ROLE_PERMISSION_CREATE,
    ),
    RP(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=value.ROLE_PERMISSION_DELETE,
    ),
    RP(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=value.PERMISSION_READ,
    ),
    RP(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=value.PERMISSION_UPDATE,
    ),
    RP(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=value.USER_READ),
    RP(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=value.USER_RESTORE),
    RP(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=value.USER_UPDATE),
    RP(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=value.USER_DELETE),
]
