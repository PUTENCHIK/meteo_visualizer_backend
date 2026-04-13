from uuid import UUID

from src.schemas import CreateRolePermissionSchema as RP
from src.utils.permissions import SystemPermission as value

INITIAL_ROLES_PERMISSIONS = [
    RP(role_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"), permission=value.USER_READ),
    RP(role_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"), permission=value.ROLE_READ),
    RP(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=value.USER_CREATE),
    RP(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=value.ROLE_CREATE),
    RP(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=value.ROLE_UPDATE),
    RP(role_id=UUID("24bc9172186d4a3383a7289ef09983c5"), permission=value.ROLE_DELETE),
]
