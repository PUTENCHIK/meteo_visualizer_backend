from pydantic import ConfigDict

from src.schemas.base import BaseSchema
from src.schemas.users import LoginSchema, NamesSchema, PasswordSchema


class SigninSchema(LoginSchema, PasswordSchema):
    pass


class SignupSchema(NamesSchema, LoginSchema, PasswordSchema):
    pass


class AuthTokensSchema(BaseSchema):
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(populate_by_name=True)
