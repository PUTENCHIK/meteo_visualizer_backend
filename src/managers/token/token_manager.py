from typing import Optional, Tuple
from uuid import UUID

import redis.asyncio as redis
from redis import Redis

from src.managers.token.tokens import AccessToken, AuthToken, RefreshToken
from src.utils import SingletonMetaclass


class TokenManager(metaclass=SingletonMetaclass):
    """
    Менеджер-сингтон для управления токенами приложения с помощью Redis
    """

    REFRESH_PREFIX = "refresh"
    BLOCKED_PREFIX = "blocked"

    __redis_client: Redis = redis.from_url("redis://localhost", decode_responses=True)

    @property
    def client(self) -> Redis:
        return self.__redis_client

    def __init__(self):
        pass

    def __refresh_token(self, user_id: UUID) -> str:
        return f"{self.REFRESH_PREFIX}:{user_id}"

    def __blocked_token(self, jti: UUID) -> str:
        return f"{self.BLOCKED_PREFIX}:{jti}"

    async def set_refresh_token(self, token: RefreshToken):
        await self.client.setex(
            self.__refresh_token(token.sub), token.exp_seconds, str(token.jti)
        )

    async def get_refresh_token(self, user_id: UUID) -> Optional[str]:
        return await self.client.get(self.__refresh_token(user_id))

    async def block_token(self, token: AuthToken):
        await self.client.setex(
            self.__blocked_token(token.jti), token.exp_seconds, "true"
        )

    async def is_blocked(self, token: AuthToken) -> bool:
        return await self.client.exists(self.__blocked_token(token.jti)) > 0

    def generate_tokens(self, user_id: UUID) -> Tuple[AccessToken, RefreshToken]:
        access_token = AccessToken(user_id)
        refresh_token = RefreshToken(user_id)

        return access_token, refresh_token
