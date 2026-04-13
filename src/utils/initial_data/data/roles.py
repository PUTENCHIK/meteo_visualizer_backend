from uuid import UUID

from src.schemas.roles import CreateRoleSchema

INITIAL_ROLES = [
    CreateRoleSchema(
        id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"), name="Пользователь", parent_id=None
    ),
    CreateRoleSchema(
        id=UUID("24bc9172186d4a3383a7289ef09983c5"),
        name="Администратор",
        parent_id=UUID("af03a5cc6f4d4a52aedb26092e88bcc3"),
    ),
]
