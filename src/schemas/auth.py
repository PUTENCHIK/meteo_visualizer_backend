from uuid import UUID

from src.schemas.base import AuditableModelSchema, BaseSchema


class NamesSchema(BaseSchema):
    lastname: str
    firstname: str
    secondname: str


class LoginSchema(BaseSchema):
    login: str


class PasswordSchema(BaseSchema):
    password: str


class SigninSchema(LoginSchema, PasswordSchema):
    pass


class UserBaseSchema(NamesSchema, LoginSchema):
    role_id: UUID


class SignupSchema(UserBaseSchema, PasswordSchema):
    pass


class UserSchema(AuditableModelSchema, UserBaseSchema):
    pass


class RefreshTokenSchema(BaseSchema):
    refresh_token: str


class AuthTokensSchema(RefreshTokenSchema):
    access_token: str
    token_type: str = "bearer"

    class Config:
        populate_by_name = True
