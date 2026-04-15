from typing import Optional
from uuid import UUID

from fastapi import Response

from src.auth.enums import SystemPermission
from src.auth.tokens import RefreshToken
from src.managers import PasswordManager, TokenManager
from src.models import User
from src.repositories import RoleRepository, UserRepository
from src.schemas import AuthTokensSchema, SigninSchema, SignupSchema
from src.utils.constants import SIGNUP_ROLE_ID
from src.utils.exceptions import (
    InvalidPasswordException,
    InvalidRefreshTokenException,
    LoginAlreadyUsesException,
    PermissionDeniedException,
    RoleNotSetException,
    TokenBlockedException,
    UserNotFoundException,
)


class AuthService:
    """
    Сервис авторизации
    """

    __user_repo: UserRepository
    __role_repo: RoleRepository
    __token_manager: TokenManager = TokenManager()
    __password_manager: PasswordManager = PasswordManager()

    @property
    def user_repo(self) -> UserRepository:
        return self.__user_repo

    @property
    def role_repo(self) -> RoleRepository:
        return self.__role_repo

    @property
    def token_manager(self) -> TokenManager:
        return self.__token_manager

    @property
    def password_manager(self) -> PasswordManager:
        return self.__password_manager

    def __init__(self, user_repo: UserRepository, role_repo: RoleRepository):
        self.__user_repo = user_repo
        self.__role_repo = role_repo

    @staticmethod
    def set_response_cookie(response: Response, refresh_token: RefreshToken):
        response.set_cookie(
            key="refresh_token",
            value=refresh_token.jwt,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=refresh_token.exp_seconds,
        )

    async def signin(self, data: SigninSchema, response: Response) -> AuthTokensSchema:
        user = await self.user_repo.get_by_login(data.login)
        if not user:
            raise UserNotFoundException(login=data.login)
        if not self.password_manager.verify_password(data.password, user.password_hash):
            raise InvalidPasswordException()

        access, refresh = self.token_manager.generate_tokens(user.id)

        await self.token_manager.set_refresh_token(refresh)
        AuthService.set_response_cookie(response, refresh)

        return AuthTokensSchema(access_token=access.jwt)

    async def signup(self, data: SignupSchema) -> User:
        user = await self.user_repo.get_by_login(data.login)
        if user:
            raise LoginAlreadyUsesException(data.login)

        password_hash = self.password_manager.hash_password(data.password)

        new_user = User(
            **data.model_dump(exclude={"password"}),
            role_id=SIGNUP_ROLE_ID,
            password_hash=password_hash,
        )
        db_user = await self.user_repo.add(new_user)
        await self.user_repo.commit()

        return await self.user_repo.get_by_id(db_user.id)

    async def refresh(
        self, refresh_jwt: Optional[str], response: Response
    ) -> AuthTokensSchema:
        if refresh_jwt is None:
            raise InvalidRefreshTokenException()

        refresh_token = RefreshToken.decode(refresh_jwt)

        saved_jti = await self.token_manager.get_refresh_token(refresh_token.sub)
        saved_jti = UUID(saved_jti) if saved_jti else None

        if saved_jti is None or saved_jti != refresh_token.jti:
            raise InvalidRefreshTokenException()

        if await self.token_manager.is_blocked(refresh_token):
            raise TokenBlockedException()

        new_access, new_refresh = self.token_manager.generate_tokens(refresh_token.sub)

        await self.token_manager.set_refresh_token(new_refresh)
        await self.token_manager.block_token(refresh_token)

        AuthService.set_response_cookie(response, new_refresh)

        return AuthTokensSchema(access_token=new_access.jwt)

    async def has_permission(self, user: User, permission: SystemPermission) -> bool:
        if not user.role:
            raise RoleNotSetException(user.id)

        all_permissions = await self.role_repo.get_role_permissions(user.role_id)
        has_perm = any(p.name == permission.value for p in all_permissions)

        if not has_perm:
            raise PermissionDeniedException(permission)

        return has_perm
