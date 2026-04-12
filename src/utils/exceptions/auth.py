from src.utils.exceptions.base import (NotFoundException, UnauthorizedException,
                                       ConflictException)


class UserNotFoundException(NotFoundException):
    def __init__(self, login: str):
        super().__init__(f"Пользователь '{login}' не найден")


class InvalidPasswordException(UnauthorizedException):
    def __init__(self):
        super().__init__("Введён неверный пароль")


class LoginAlreadyUsesException(ConflictException):
    def __init__(self, login: str):
        super().__init__(f"Логин '{login}' уже используется")