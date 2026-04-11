from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from uuid import UUID

import jwt

from src.managers.token.tokens.abstract_token import AbstractToken


class AuthToken(AbstractToken):
    """
    Абстрактная модель токена авторизации
    """

    SECRET_KEY = "a2387f975d59c03080284689f4de177e607db84932b1386f8d126c20b0f29137"
    ALGORITHM = "HS256"

    __sub: UUID
    __exp_time: datetime
    __exp_seconds: int

    @property
    def sub(self) -> UUID:
        return self.__sub

    @property
    def exp_time(self) -> datetime:
        return self.__exp_time

    @property
    def exp_seconds(self) -> int:
        return self.__exp_seconds

    def __init__(self, sub: UUID, exp: int):
        super().__init__()
        self.__sub = sub
        self.__exp_seconds = exp
        self.__exp_time = datetime.now(timezone.utc) + timedelta(seconds=exp)

    @property
    def payload(self) -> Dict[str, Any]:
        return {
            "jti": str(self.jti),
            "sub": str(self.sub),
            "exp": self.exp_time,
            "type": str(self.type),
        }

    @property
    def jwt(self) -> str:
        return jwt.encode(self.payload, self.SECRET_KEY, self.ALGORITHM)
