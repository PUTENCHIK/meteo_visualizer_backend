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