from typing import List, Optional

from src.auth.enums import SystemPermission
from src.schemas.base import BaseSchema


class InitialRoleSchema(BaseSchema):
    name: str
    parent_name: Optional[str] = None
    permissions: List[SystemPermission]


class InitialUserSchema(BaseSchema):
    lastname: str
    firstname: str
    secondname: Optional[str] = None
    login: str
    role_name: str


class InitialDataSchema(BaseSchema):
    roles: List[InitialRoleSchema]
    users: List[InitialUserSchema]
    base_role_name: str
