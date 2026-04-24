from uuid import UUID

from src.auth.enums import SystemPermission, TokenType
from src.utils.exceptions.code.exception_code import ExceptionCode
from src.utils.exceptions.core.base import (
    ConflictException,
    ForbiddenException,
    UnauthorizedException,
)


class InvalidPasswordException(UnauthorizedException):
    code = ExceptionCode.INVALID_CREDENTIALS

    def __init__(self):
        super().__init__("Введён неверный пароль")


class LoginAlreadyUsesException(ConflictException):
    code = ExceptionCode.INVALID_CREDENTIALS

    def __init__(self, login: str):
        super().__init__(f"Логин '{login}' уже используется")


class InvalidAccessTokenException(UnauthorizedException):
    code = ExceptionCode.TOKEN_INVALID

    def __init__(self):
        super().__init__("Токен доступа некорректен")


class InvalidRefreshTokenException(UnauthorizedException):
    code = ExceptionCode.TOKEN_INVALID

    def __init__(self):
        super().__init__("Токен для обновления некорректен")


class TokenExpiredException(UnauthorizedException):
    code = ExceptionCode.TOKEN_EXPIRED

    def __init__(self):
        super().__init__("Токен доступа истёк")


class TokenBlockedException(UnauthorizedException):
    code = ExceptionCode.TOKEN_INVALID

    def __init__(self):
        super().__init__("Токен доступа заблокирован")


class InvalidTokenTypeException(UnauthorizedException):
    code = ExceptionCode.TOKEN_INVALID

    def __init__(self, value: TokenType, expected: TokenType):
        super().__init__(f"Неверный тип токена {value}, ожидался {expected}")


class TokenMissingException(UnauthorizedException):
    code = ExceptionCode.TOKEN_INVALID

    def __init__(self):
        super().__init__("Токен доступа не получен")

class RoleNotSetException(ForbiddenException):
    def __init__(self, user_id: UUID):
        super().__init__(f"У пользователя ({user_id.hex[:8]}) не назначена роль")


class PermissionDeniedException(ForbiddenException):
    def __init__(self, need_perm: SystemPermission):
        super().__init__(
            f"Доступ запрещён, необходимо обладать разрешением '{need_perm.value}'"
        )
