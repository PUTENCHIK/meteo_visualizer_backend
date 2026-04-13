from abc import abstractmethod
from typing import List, TypeVar, override
from uuid import UUID

from src.models import AuditableModel
from src.repositories import AuditableRepository
from src.services.abstractions.base_service import BaseService
from src.utils.exceptions import NotFoundException

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

    @override
    async def get_all(self, include_deleted: bool = False) -> List[A]:
        return await self._repository.get_all(include_deleted)

    async def get_by_id(self, id_: UUID, include_deleted: bool = False) -> A:
        entity = self._repository.get_by_id(id_, include_deleted)
        if not entity:
            raise NotFoundException()
        return entity

    async def _create(self, entity: A) -> A:
        entity = await self._repository.add(entity)
        await self._repository.commit_refresh(entity)
        return entity

    async def _restore(self, entity: A) -> A:
        entity = await self._repository.restore(entity)
        await self._repository.commit_refresh(entity)
        return entity

    async def _delete(self, entity: A, force: bool = False):
        await self._repository.delete(entity, force)
        await self._repository.commit()
