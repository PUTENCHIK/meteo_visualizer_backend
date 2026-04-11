from abc import abstractmethod
from typing import List, TypeVar

from src.models import AuditableModel
from src.repositories import AuditableRepository
from src.services.abstractions.base_service import BaseService

A = TypeVar("A", bound=AuditableModel)
R = TypeVar("R", bound=AuditableRepository)


class AuditableService(BaseService[A, R]):
    """
    Расширение для базового сервиса для сущностей типа AuditableModel
    """

    _repository: R

    @property
    def repository(self) -> R:
        return self._repository

    @abstractmethod
    def __init__(self, repository: R):
        super().__init__(repository)

    async def get_all(self, include_deleted: bool = False) -> List[A]:
        return await self._repository.get_all(include_deleted)
