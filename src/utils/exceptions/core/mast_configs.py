from uuid import UUID

from src.utils.exceptions.core.base import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)


class MastConfigNotFoundException(NotFoundException):
    def __init__(self, id_: UUID):
        super().__init__(f"Конфиг мачты ({id_.hex[:8]}) не найден")


class MastConfigNotDeletedException(BadRequestException):
    def __init__(self, id_: UUID):
        super().__init__(f"Конфиг мачты ({id_.hex[:8]}) не удалён")


class MastConfigHasActiveMastsException(ConflictException):
    def __init__(self, id_: UUID, count: int):
        super().__init__(
            f"Конфиг мачты ({id_.hex[:8]}) используется мачтами ({count}) "
            f"и не может быть удалён"
        )


class MastConfigTooLowException(BadRequestException):
    def __init__(self, height: int):
        super().__init__(f"Высота не может быть ниже, чем высота реи - {height}м")
