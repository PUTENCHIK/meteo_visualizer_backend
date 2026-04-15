from uuid import UUID

from src.utils.exceptions.core.base import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)


class MastYardNotFoundException(NotFoundException):
    def __init__(self, id_: UUID):
        super().__init__(f"Рея мачты ({id_.hex[:8]}) не найдена")


class InvalidMastYardHeightException(BadRequestException):
    def __init__(self, height: int):
        super().__init__(f"Высота реи не может быть больше высоты мачты: {height}м")


class MastYardAlreadyExistsException(ConflictException):
    def __init__(self, config_name: str, height: int):
        super().__init__(f"У конфига '{config_name}' уже есть рея на высоте {height}м")
