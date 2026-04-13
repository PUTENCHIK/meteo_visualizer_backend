from abc import ABC, abstractmethod
from uuid import UUID, uuid4

from src.managers.token.tokens.token_type import TokenType


class AbstractToken(ABC):
    """
    Абстрактрая модель токена приложения
    """

    _jti: UUID

    @property
    def jti(self) -> UUID:
        return self._jti

    @property
    @abstractmethod
    def type(self) -> TokenType:
        pass

    def __init__(self):
        super().__init__()
        self._jti = uuid4()
