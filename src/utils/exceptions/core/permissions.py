from typing import Optional
from uuid import UUID

from src.utils.exceptions.core.base import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)


class PermissionNameAlreadyExistsException(ConflictException):
    def __init__(self, name: str):
        super().__init__(f"Разрешение '{name}' уже существует")


class PermissionNotFoundException(NotFoundException):
    def __init__(self, id_: Optional[UUID] = None, name: Optional[str] = None):
        if id_ is not None:
            idtf = f" ({id_.hex[:8]})"
        elif name is not None:
            idtf = f" '{name}'"
        else:
            idtf = ""
        super().__init__(f"Разрешение{idtf} не найдено")


class PermissionNotDeletedException(BadRequestException):
    def __init__(self, id_: UUID):
        super().__init__(f"Разрешение ({id_.hex[:8]}) не удалено")
