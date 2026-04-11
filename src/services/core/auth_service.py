from src.managers import PasswordManager, TokenManager
from src.models import User
from src.repositories import UserRepository
from src.schemas import AuthTokensSchema, SigninSchema, SignupSchema
from src.utils.exceptions import (
    InvalidPasswordException,
    LoginAlreadyUsesException,
    UserNotFoundException,
)


class AuthService:
    """
    Сервис авторизации
    """

    __user_repo: UserRepository
    __token_manager: TokenManager = TokenManager()
    __password_manager: PasswordManager = PasswordManager()

    @property
    def user_repo(self) -> UserRepository:
        return self.__user_repo

    @property
    def token_manager(self) -> TokenManager:
        return self.__token_manager

    def __init__(self, user_repository: UserRepository):
        self.__user_repo = user_repository

    async def signin(self, data: SigninSchema) -> AuthTokensSchema:
        user = await self.user_repo.get_by_login(data.login)
        if not user:
            raise UserNotFoundException(data.login)
        if not self.__password_manager.verify_password(
            data.password, user.password_hash
        ):
            raise InvalidPasswordException()

        access, refresh = self.token_manager.generate_tokens(user.id)

        await self.token_manager.set_refresh_token(refresh)

        return AuthTokensSchema(access=access.jwt, refresh=refresh.jwt)

    async def signup(self, data: SignupSchema) -> User:
        user = await self.user_repo.get_by_login(data.login)
        if user:
            raise LoginAlreadyUsesException(data.login)

        password_hash = self.__password_manager.hash_password(data.password)

        new_user = User(
            **data.model_dump(exclude={"password"}), password_hash=password_hash
        )

        return await self.user_repo.add(new_user)
