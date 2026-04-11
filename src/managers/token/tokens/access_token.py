from uuid import UUID

from src.managers.token.tokens.auth_token import AuthToken
from src.managers.token.tokens.token_type import TokenType


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
