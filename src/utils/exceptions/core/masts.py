from uuid import UUID

from src.utils.exceptions.core.base import NotFoundException


class MastNotFoundException(NotFoundException):
    def __init__(self, id_: UUID):
        super().__init__(f"Мачта комплекса ({id_.hex[:8]}) не найдена")
