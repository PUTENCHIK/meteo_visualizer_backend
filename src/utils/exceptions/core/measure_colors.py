from uuid import UUID

from src.utils.exceptions.core.base import BadRequestException, NotFoundException


class MeasureColorNotFoundException(NotFoundException):
    def __init__(self, id_: UUID):
        super().__init__(f"Цвет параметра ({id_.hex[:8]}) не найден")


class MeasureColorAlreadyExistsException(BadRequestException):
    def __init__(self, measure_name: UUID, percent: float):
        super().__init__(
            f"Для параметра '{measure_name}' уже установлен цвет в {percent}"
        )


class MaxMeasureColorsException(BadRequestException):
    def __init__(self, measure_name: str, limit: int):
        super().__init__(
            f"Предел в {limit} цветов у параметра {measure_name} достигнут"
        )
