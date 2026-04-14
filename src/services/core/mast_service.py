from typing import override
from uuid import UUID

from src.models import Mast
from src.repositories import ComplexRepository, MastConfigRepository, MastRepository
from src.schemas import CreateMastSchema, UpdateMastSchema
from src.services.abstractions.auditable_service import AuditableService
from src.utils.exceptions import (
    ComplexNotFoundException,
    MastConfigNotFoundException,
    MastNotFoundException,
)


class MastService(AuditableService[Mast, MastRepository]):
    """
    Сервис мачт комплексов
    """

    __complex_repo: ComplexRepository
    __config_repo: MastConfigRepository

    @property
    def complex_repo(self) -> ComplexRepository:
        return self.__complex_repo

    @property
    def config_repo(self) -> MastConfigRepository:
        return self.__config_repo

    def __init__(
        self,
        repository: MastRepository,
        complex_repo: ComplexRepository,
        config_repo: MastConfigRepository,
    ):
        super().__init__(repository)
        self.__complex_repo = complex_repo
        self.__config_repo = config_repo

    @override
    async def get_by_id(self, id_, include_deleted=False) -> Mast:
        mast = await self.repository.get_by_id(id_, include_deleted)
        if not mast:
            raise MastNotFoundException(id_)
        return mast

    async def create_mast(self, data: CreateMastSchema) -> Mast:
        complex = await self.complex_repo.get_by_id(data.complex_id)
        if not complex:
            raise ComplexNotFoundException(data.complex_id)

        config = await self.config_repo.get_by_id(data.config_id)
        if not config:
            raise MastConfigNotFoundException(data.config_id)

        new_mast = Mast(**data.model_dump())
        created_mast = await self._create(new_mast)

        return await self.get_by_id(created_mast.id)

    async def update_mast(self, id_: UUID, data: UpdateMastSchema) -> Mast:
        mast = await self.get_by_id(id_)

        if data.config_id is not None:
            config = await self.config_repo.get_by_id(data.config_id)
            if not config:
                raise MastConfigNotFoundException(data.config_id)

        return await self._update(mast, data)

    async def delete_mast(self, id_: UUID):
        mast = await self.get_by_id(id_)

        await self._delete(mast)
