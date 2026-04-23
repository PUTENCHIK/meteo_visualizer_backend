from abc import abstractmethod
from datetime import datetime, timezone
from typing import List, Optional, TypeVar, override
from uuid import UUID

from sqlalchemy.orm import with_loader_criteria

from src.models import AuditableModel
from src.repositories.abstractions.base_repository import BaseRepository

A = TypeVar("A", bound=AuditableModel)


class AuditableRepository(BaseRepository[A]):
    """
    Расширение для базового репозитория для сущностей типа AuditableModel
    """

    @abstractmethod
    def __init__(self, model, session):
        super().__init__(model, session)

    async def get_by_id(self, id_: UUID, include_deleted: bool = False) -> Optional[A]:
        statement = self._get_all_query(include_deleted).where(self.model.id == id_)

        return (await self.session.exec(statement)).one_or_none()

    @override
    def _get_all_query(self, include_deleted: bool = False):
        statement = super()._get_all_query()
        if not include_deleted:
            statement = statement.options(
                with_loader_criteria(
                    AuditableModel,
                    lambda cls: getattr(cls, "deleted_at", None) == None,
                    include_aliases=True
                )
            )
        return statement.order_by(self.model.updated_at.desc())

    @override
    async def get_all(self, include_deleted: bool = False) -> List[A]:
        result = await self.session.exec(self._get_all_query(include_deleted))
        return result.all()

    @override
    async def delete(self, obj: A, force: bool = False) -> bool:
        if force:
            return await super().delete(obj)
        else:
            obj.deleted_at = datetime.now(timezone.utc)
            self.session.add(obj)
            return True

    async def restore(self, obj: A) -> A:
        obj.deleted_at = None
        self.session.add(obj)
        await self.session.flush()
        return obj
