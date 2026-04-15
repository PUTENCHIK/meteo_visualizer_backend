from uuid import UUID

from src.utils.exceptions.core.base import BadRequestException, NotFoundException


class ComplexNotFoundException(NotFoundException):
    def __init__(self, id_: UUID):
        super().__init__(f"Комплекс ({id_.hex[:8]}) не найден")


class ComplexNotDeletedException(BadRequestException):
    def __init__(self, id_: UUID):
        super().__init__(f"Комплекс ({id_.hex[:8]}) не удалён")
