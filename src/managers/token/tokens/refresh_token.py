from uuid import UUID

from src.managers.token.tokens.auth_token import AuthToken
from src.managers.token.tokens.token_type import TokenType


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
