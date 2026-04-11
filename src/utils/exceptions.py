from uuid import UUID


class AppException(Exception):
    """
    Базовое исключение приложения
    """

    status_code = 500

    def __init__(self, message: str):
        super().__init__(message)


class BadRequestException(AppException):
    """
    Статус (400)
    """

    status_code = 400

    def __init__(self, message: str = "Некорректный запрос"):
        super().__init__(message)


class UnauthorizedException(AppException):
    """
    Статус (401)
    """

    status_code = 401

    def __init__(self, message: str = "Не авторизован"):
        super().__init__(message)


class ForbiddenException(AppException):
    """
    Статус (403)
    """

    status_code = 403

    def __init__(self, message: str = "Запрещено"):
        super().__init__(message)


class NotFoundException(AppException):
    """
    Статус (404)
    """

    status_code = 404

    def __init__(self, message: str = "Не найдено"):
        super().__init__(message)


class ConflictException(AppException):
    """
    Статус (409)
    """

    status_code = 409

    def __init__(self, message: str = "Конфликт"):
        super().__init__(message)


class UserNotFoundException(NotFoundException):
    def __init__(self, login: str):
        super().__init__(f"Пользователь '{login}' не найден")


class InvalidPasswordException(UnauthorizedException):
    def __init__(self):
        super().__init__("Введён неверный пароль")


class LoginAlreadyUsesException(ConflictException):
    def __init__(self, login: str):
        super().__init__(f"Логин '{login}' уже используется")


class RoleNameAlreadyExistsException(ConflictException):
    def __init__(self, name: str):
        super().__init__(f"Роль '{name}' уже существует")


class RoleNotFoundException(NotFoundException):
    def __init__(self, id_: UUID):
        super().__init__(f"Роль ({id_.hex[:8]}) не найдена")


class RoleParentCantBeSameException(BadRequestException):
    def __init__(self):
        super().__init__("Роль не может иметь в качестве родителя саму себя")


class RoleNotDeletedException(BadRequestException):
    def __init__(self, id_: UUID):
        super().__init__(f"Роль ({id_.hex[:8]}) не удалена")
