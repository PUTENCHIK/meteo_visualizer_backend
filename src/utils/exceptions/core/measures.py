from uuid import UUID

from src.utils.exceptions.core.base import BadRequestException, NotFoundException


class MeasureNotFoundException(NotFoundException):
    def __init__(self, id_: UUID):
        super().__init__(f"Пользовательский параметр ({id_.hex[:8]}) не найден")


class MeasureNotDeletedException(BadRequestException):
    def __init__(self, id_: UUID):
        super().__init__(f"Пользовательский параметр ({id_.hex[:8]}) не удалён")


class InvalidMeasureScaleException(BadRequestException):
    def __init__(self, min: int, max: int):
        super().__init__(f"Минимум должен быть меньше максимума: ({min}, {max})")
