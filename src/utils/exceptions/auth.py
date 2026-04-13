from typing import Optional
from uuid import UUID

from src.managers.token.tokens.token_type import TokenType
from src.utils.exceptions.base import (
    ConflictException,
    NotFoundException,
    UnauthorizedException,
)


class UserNotFoundException(NotFoundException):
    def __init__(self, id_: Optional[UUID] = None, login: Optional[str] = None):
        if id_ is not None:
            idtf = f" ({id_.hex[:8]})"
        elif login is not None:
            idtf = f" '{login}'"
        else:
            idtf = ""
        super().__init__(f"Пользователь{idtf} не найден")


class InvalidPasswordException(UnauthorizedException):
    def __init__(self):
        super().__init__("Введён неверный пароль")


class LoginAlreadyUsesException(ConflictException):
    def __init__(self, login: str):
        super().__init__(f"Логин '{login}' уже используется")


class InvalidTokenException(UnauthorizedException):
    def __init__(self):
        super().__init__("Токен доступа некорректен")


class TokenExpiredException(UnauthorizedException):
    def __init__(self):
        super().__init__("Токен доступа истёк")


class TokenBlockedException(UnauthorizedException):
    def __init__(self):
        super().__init__("Токен доступа заблокирован")


class InvalidTokenTypeException(UnauthorizedException):
    def __init__(self, value: TokenType, expected: TokenType):
        super().__init__(f"Неверный тип токена {value}, ожидался {expected}")
