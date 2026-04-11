from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from src.models import Base
from src.repositories import BaseRepository

T = TypeVar("T", bound=Base)
R = TypeVar("R", bound=BaseRepository)


class BaseService(ABC, Generic[T, R]):
    """
    Абстрактный класс базового сервиса
    """

    _repository: R

    @property
    def repository(self) -> R:
        return self._repository

    @abstractmethod
    def __init__(self, repository: R):
        super().__init__()
        self._repository = repository

    @abstractmethod
    def get_all(self) -> List[T]:
        pass
