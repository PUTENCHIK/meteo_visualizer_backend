from uuid import UUID

from src.utils.exceptions.core.base import NotFoundException


class MastNotFoundException(NotFoundException):
    def __init__(self, id_: UUID):
        super().__init__(f"Мачта комплекса ({id_.hex[:8]}) не найдена")


class MastHasSamePrefixException(NotFoundException):
    def __init__(self, prefix: str, mast_id: UUID):
        super().__init__(
            f"У комплекса уже есть мачта с префиксом '{prefix}' - ({mast_id.hex[:8]})"
        )
