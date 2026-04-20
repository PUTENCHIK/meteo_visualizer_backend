from uuid import UUID

from src.auth.enums import SystemPermission as value
from src.schemas import CreateRolePermissionSchema as RP

INITIAL_ROLES_PERMISSIONS = [
    RP(role_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"), permission=value.ROLE_READ),
    RP(role_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"), permission=value.COMPLEX_READ),
    RP(role_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"), permission=value.MAST_READ),
    RP(
        role_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"),
        permission=value.MAST_CONFIG_READ,
    ),
    RP(
        role_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"),
        permission=value.MAST_YARD_READ,
    ),
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
    RP(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=value.COMPLEX_CREATE,
    ),
    RP(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=value.COMPLEX_RESTORE,
    ),
    RP(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=value.COMPLEX_UPDATE,
    ),
    RP(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=value.COMPLEX_DELETE,
    ),
    RP(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=value.MAST_CREATE),
    RP(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=value.MAST_UPDATE),
    RP(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=value.MAST_DELETE),
    RP(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=value.MAST_CONFIG_CREATE,
    ),
    RP(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=value.MAST_CONFIG_RESTORE,
    ),
    RP(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=value.MAST_CONFIG_UPDATE,
    ),
    RP(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=value.MAST_CONFIG_DELETE,
    ),
    RP(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=value.MAST_YARD_CREATE,
    ),
    RP(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=value.MAST_YARD_UPDATE,
    ),
    RP(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=value.MAST_YARD_DELETE,
    ),
    RP(
        role_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"),
        permission=value.COMPLEX_FAVORITE_CREATE,
    ),
    RP(
        role_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"),
        permission=value.COMPLEX_FAVORITE_DELETE,
    ),
]
