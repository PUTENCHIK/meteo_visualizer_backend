from uuid import UUID

import jwt

from src.auth.enums import TokenType
from src.auth.tokens.auth_token import AuthToken
from src.config import config
from src.utils.exceptions import InvalidTokenException, TokenExpiredException


class AccessToken(AuthToken):
    """
    Быстроистекающий токен доступа
    """

    TOKEN_EXPIRE_MINUTES = 15

    @property
    def type(self) -> TokenType:
        return TokenType.ACCESS

    def __init__(self, sub: UUID):
        super().__init__(sub, self.TOKEN_EXPIRE_MINUTES * 60)

    @staticmethod
    def decode(jwt_token: str) -> "AccessToken":
        try:
            payload = jwt.decode(
                jwt_token,
                config.auth_token_secret_key,
                algorithms=[config.auth_token_algorithm],
            )
            return AccessToken.new(payload, TokenType.ACCESS)
        except jwt.DecodeError:
            raise InvalidTokenException()
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException()
