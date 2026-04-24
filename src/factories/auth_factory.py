from typing import Optional
from fastapi import Depends, Request, Query, WebSocket
from fastapi.security import OAuth2PasswordBearer

from src.auth.tokens import AccessToken
from src.factories.service_factory import ServiceFactory
from src.managers import TokenManager
from src.models import User
from src.services import UserService
from src.utils.exceptions import TokenBlockedException, TokenMissingException


class AuthFactory:
    """
    Фабрика для методов авторизации
    """

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/signin")

    @staticmethod
    async def get_user_by_token(
        token: str,
        user_service: UserService,
    ) -> User:
        token_manager = TokenManager()
        access_token = AccessToken.decode(token)

        if await token_manager.is_blocked(access_token):
            raise TokenBlockedException()

        return await user_service.get_by_id(access_token.sub)

    @staticmethod
    async def get_current_user(
        token: str = Depends(oauth2_scheme),
        user_service: UserService = Depends(ServiceFactory.get_user_service),
    ) -> User:
        return await AuthFactory.get_user_by_token(token, user_service)
    get_user_by_token
    @staticmethod
    async def get_query_user(
        user_service: UserService,
        token: Optional[str] = None,
    ) -> User:
        if not token:
            raise TokenMissingException()

        return await AuthFactory.get_user_by_token(token, user_service)
