from uuid import UUID

from src.utils.exceptions.core.base import BadRequestException, NotFoundException


class MeasureAliasNotFoundException(NotFoundException):
    def __init__(self, id_: UUID):
        super().__init__(f"Псевдоним параметра ({id_.hex[:8]}) не найден")


class MeasureAliasAlreadyExistsException(BadRequestException):
    def __init__(self, measure_name: str, name: str):
        super().__init__(
            f"Для параметра '{measure_name}' уже существует псевдоним '{name}'"
        )
