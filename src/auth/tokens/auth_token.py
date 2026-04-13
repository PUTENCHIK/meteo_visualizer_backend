from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Self
from uuid import UUID

import jwt

from src.auth.enums import TokenType
from src.auth.tokens.abstract_token import AbstractToken
from src.config import config
from src.utils.exceptions import InvalidTokenException, InvalidTokenTypeException


class AuthToken(AbstractToken):
    """
    Абстрактная модель токена авторизации
    """

    _sub: UUID
    _exp_time: datetime
    _exp_seconds: int

    @property
    def sub(self) -> UUID:
        return self._sub

    @property
    def exp_time(self) -> datetime:
        return self._exp_time

    @property
    def exp_seconds(self) -> int:
        return self._exp_seconds

    def __init__(self, sub: UUID, exp: int):
        super().__init__()
        self._sub = sub
        self._exp_seconds = exp
        self._exp_time = datetime.now(timezone.utc) + timedelta(seconds=exp)

    @property
    def payload(self) -> Dict[str, Any]:
        return {
            "jti": str(self.jti),
            "sub": str(self.sub),
            "exp": int(self.exp_time.timestamp()),
            "type": str(self.type.value),
        }

    @property
    def jwt(self) -> str:
        return jwt.encode(
            self.payload, config.auth_token_secret_key, config.auth_token_algorithm
        )

    @classmethod
    def new(cls, payload: Dict[str, Any], expected_type: TokenType) -> Self:
        try:
            sub = UUID(payload["sub"])
            jti = UUID(payload["jti"])
            exp_timestamp = payload["exp"]
            type_ = TokenType(payload["type"])
            if type_ != expected_type:
                raise InvalidTokenTypeException(type_, expected_type)

            instance = cls(sub)

            instance._jti = jti
            instance._exp_time = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)

            return instance
        except (KeyError, ValueError, TypeError):
            raise InvalidTokenException()
