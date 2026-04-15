from src.schemas.base import BaseSchema
from src.schemas.users import LoginSchema, NamesSchema, PasswordSchema


class SigninSchema(LoginSchema, PasswordSchema):
    pass


class SignupSchema(NamesSchema, LoginSchema, PasswordSchema):
    pass


class AuthTokensSchema(BaseSchema):
    access_token: str
    token_type: str = "bearer"

    class Config:
        populate_by_name = True
