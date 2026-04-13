from uuid import UUID

import jwt

from src.managers.token.tokens.auth_token import AuthToken
from src.managers.token.tokens.token_type import TokenType
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
                jwt_token, AccessToken.SECRET_KEY, algorithms=[AccessToken.ALGORITHM]
            )
            return AccessToken.new(payload, TokenType.ACCESS)
        except jwt.DecodeError:
            raise InvalidTokenException()
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException()
