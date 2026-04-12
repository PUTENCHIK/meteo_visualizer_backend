from abc import ABC, abstractmethod
from typing import Generic, List, Type, TypeVar

from pydantic import BaseModel
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import Base

T = TypeVar("T", bound=Base)


class BaseRepository(ABC, Generic[T]):
    """
    Абстрактный класс базового репозитория для любой сущности
    """

    _model: Type[T]
    _session: AsyncSession

    @property
    def model(self) -> Type[T]:
        return self._model

    @property
    def session(self) -> AsyncSession:
        return self._session

    @abstractmethod
    def __init__(self, model: Type[T], session: AsyncSession):
        super().__init__()
        self._model = model
        self._session = session

    def _get_all_query(self):
        return select(self.model)

    async def get_all(self) -> List[T]:
        result = await self.session.exec(self._get_all_query())
        return result.all()

    async def add(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.flush()
        return obj
    
    async def add_many(self, objects: List[T]) -> List[T]:
        self.session.add_all(objects)
        await self.session.flush()
        return objects

    async def update(self, db_obj: T, data: BaseModel) -> T:
        update_data = data.model_dump(exclude_unset=True)

        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])

        self.session.add(db_obj)
        await self.session.flush()
        return db_obj

    async def delete(self, obj: T) -> bool:
        await self.session.delete(obj)
        await self.session.flush()
        return True
    
    async def flush(self):
        await self.session.flush()

    async def commit(self):
        await self.session.commit()
    
    async def refresh(self, obj: T):
        await self.session.refresh(obj)
    
    async def commit_refresh(self, obj: T):
        await self.session.commit()
        await self.session.refresh(obj)
