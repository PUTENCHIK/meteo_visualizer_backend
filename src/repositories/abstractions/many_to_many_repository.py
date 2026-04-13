from abc import abstractmethod
from typing import Optional, TypeVar

from src.models import ManyToManyModel
from src.repositories.abstractions.base_repository import BaseRepository

M = TypeVar("M", bound=ManyToManyModel)


class ManyToManyRepository(BaseRepository[M]):
    """
    Расширение для базового репозитория для сущностей типа ManyToManyModel
    """

    @abstractmethod
    def __init__(self, model, session):
        super().__init__(model, session)

    @abstractmethod
    async def get_by_ids(self) -> Optional[M]:
        pass
