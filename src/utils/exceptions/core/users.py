from typing import Optional
from uuid import UUID

from src.utils.exceptions.core.base import BadRequestException, NotFoundException


class UserNotFoundException(NotFoundException):
    def __init__(self, id_: Optional[UUID] = None, login: Optional[str] = None):
        if id_ is not None:
            idtf = f" ({id_.hex[:8]})"
        elif login is not None:
            idtf = f" '{login}'"
        else:
            idtf = ""
        super().__init__(f"Пользователь{idtf} не найден")


class UserNotDeletedException(BadRequestException):
    def __init__(self, id_: UUID):
        super().__init__(f"Пользователь ({id_.hex[:8]}) не удалён")
