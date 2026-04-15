from uuid import UUID

import jwt

from src.auth.enums import TokenType
from src.auth.tokens.auth_token import AuthToken
from src.config import config
from src.utils.exceptions import InvalidAccessTokenException, TokenExpiredException


class RefreshToken(AuthToken):
    """
    Долгоживущий токен для обновления токена доступа
    """

    TOKEN_EXPIRE_DAYS = 7

    @property
    def type(self) -> TokenType:
        return TokenType.REFRESH

    def __init__(self, sub: UUID):
        super().__init__(sub, self.TOKEN_EXPIRE_DAYS * 24 * 60 * 60)

    @staticmethod
    def decode(jwt_token: str) -> "RefreshToken":
        try:
            payload = jwt.decode(
                jwt_token,
                config.auth_token_secret_key,
                algorithms=[config.auth_token_algorithm],
            )
            return RefreshToken.new(payload, TokenType.REFRESH)
        except jwt.DecodeError:
            raise InvalidAccessTokenException()
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException()
