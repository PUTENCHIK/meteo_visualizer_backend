from uuid import UUID

from src.utils.exceptions.core.base import BadRequestException, NotFoundException


class MastConfigNotFoundException(NotFoundException):
    def __init__(self, id_: UUID):
        super().__init__(f"Конфиг мачты ({id_.hex[:8]}) не найден")


class MastConfigNotDeletedException(BadRequestException):
    def __init__(self, id_: UUID):
        super().__init__(f"Конфиг мачты ({id_.hex[:8]}) не удалён")
