from uuid import UUID

from src.auth.enums import SystemPermission as p
from src.schemas import CreateRolePermissionSchema as l

INITIAL_ROLES_PERMISSIONS = [
    l(role_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"), permission=p.USER_READ),
    l(role_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"), permission=p.ROLE_READ),
    l(role_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"), permission=p.COMPLEX_READ),
    l(role_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"), permission=p.MAST_READ),
    l(role_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"), permission=p.MAST_CONFIG_READ),
    l(
        role_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"),
        permission=p.MAST_YARD_READ,
    ),
    l(
        role_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"),
        permission=p.COMPLEX_WEBSOCKET,
    ),
    l(
        role_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"),
        permission=p.USER_UPDATE_SELF,
    ),
    l(
        role_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"),
        permission=p.MEASURE_READ,
    ),
    l(
        role_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"),
        permission=p.MEASURE_COLOR_READ,
    ),
    l(
        role_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"),
        permission=p.MEASURE_ALIAS_READ,
    ),
    l(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=p.ROLE_READ),
    l(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=p.COMPLEX_READ),
    l(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=p.MAST_READ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.MAST_CONFIG_READ,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.MAST_YARD_READ,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.COMPLEX_WEBSOCKET,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.USER_UPDATE_SELF,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.MEASURE_READ,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.MEASURE_COLOR_READ,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.MEASURE_ALIAS_READ,
    ),
    l(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=p.ROLE_CREATE),
    l(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=p.ROLE_RESTORE),
    l(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=p.ROLE_UPDATE),
    l(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=p.ROLE_DELETE),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.ROLE_PERMISSION_CREATE,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.ROLE_PERMISSION_DELETE,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.PERMISSION_READ,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.PERMISSION_UPDATE,
    ),
    l(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=p.USER_READ),
    l(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=p.USER_RESTORE),
    l(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=p.USER_UPDATE),
    l(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=p.USER_DELETE),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.COMPLEX_CREATE,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.COMPLEX_RESTORE,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.COMPLEX_UPDATE,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.COMPLEX_DELETE,
    ),
    l(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=p.MAST_CREATE),
    l(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=p.MAST_UPDATE),
    l(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=p.MAST_DELETE),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.MAST_CONFIG_CREATE,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.MAST_CONFIG_RESTORE,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.MAST_CONFIG_UPDATE,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.MAST_CONFIG_DELETE,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.MAST_YARD_CREATE,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.MAST_YARD_UPDATE,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.MAST_YARD_DELETE,
    ),
    l(
        role_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"),
        permission=p.COMPLEX_FAVORITE_CREATE,
    ),
    l(
        role_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"),
        permission=p.COMPLEX_FAVORITE_DELETE,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.MEASURE_CREATE,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.MEASURE_RESTORE,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.MEASURE_UPDATE,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.MEASURE_DELETE,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.MEASURE_COLOR_CREATE,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.MEASURE_COLOR_UPDATE,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.MEASURE_COLOR_DELETE,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.MEASURE_ALIAS_CREATE,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.MEASURE_ALIAS_UPDATE,
    ),
    l(
        role_id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        permission=p.MEASURE_ALIAS_DELETE,
    ),
]
