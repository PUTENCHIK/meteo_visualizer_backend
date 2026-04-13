from uuid import UUID

import jwt

from src.managers.token.tokens.auth_token import AuthToken
from src.managers.token.tokens.token_type import TokenType
from src.utils.exceptions import InvalidTokenException, TokenExpiredException


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
                jwt_token, RefreshToken.SECRET_KEY, algorithms=[RefreshToken.ALGORITHM]
            )
            return RefreshToken.new(payload, TokenType.REFRESH)
        except jwt.DecodeError:
            raise InvalidTokenException()
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException()
