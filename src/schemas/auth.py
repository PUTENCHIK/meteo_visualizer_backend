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


class AuthTokensSchema(BaseSchema):
    access: str
    refresh: str
