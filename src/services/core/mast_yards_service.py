from typing import override
from uuid import UUID

from src.models import MastYard
from src.repositories import MastConfigRepository, MastYardRepository
from src.schemas import CreateMastYardSchema, UpdateMastYardSchema
from src.services.abstractions.auditable_service import AuditableService
from src.utils.exceptions import (
    InvalidMastYardHeightException,
    MastConfigNotFoundException,
    MastYardAlreadyExistsException,
    MastYardNotFoundException,
)


class MastYardService(AuditableService[MastYard, MastYardRepository]):
    """
    Сервис рей мачт
    """

    __config_repo: MastConfigRepository

    @property
    def config_repo(self) -> MastConfigRepository:
        return self.__config_repo

    def __init__(
        self, repository: MastYardRepository, config_repo: MastConfigRepository
    ):
        super().__init__(repository)
        self.__config_repo = config_repo

    @override
    async def get_by_id(self, id_, include_deleted=False) -> MastYard:
        mast_yard = await self.repository.get_by_id(id_, include_deleted)
        if not mast_yard:
            raise MastYardNotFoundException(id_)
        return mast_yard

    async def create_mast_yard(self, data: CreateMastYardSchema) -> MastYard:
        config = await self.config_repo.get_by_id(data.config_id)

        if not config:
            raise MastConfigNotFoundException(data.config_id)

        if data.height > config.height:
            raise InvalidMastYardHeightException(config.height)

        yard = await self.repository.get_by_height(data.config_id, data.height)
        if yard:
            raise MastYardAlreadyExistsException(config.name, data.height)

        new_yard = MastYard(**data.model_dump())

        return await self._create(new_yard)

    async def update_mast_yard(self, id_: UUID, data: UpdateMastYardSchema) -> MastYard:
        yard = await self.repository.get_by_id(id_)

        if data.height > yard.config.height:
            raise InvalidMastYardHeightException(yard.config.height)

        by_height = await self.repository.get_by_height(yard.config.id, data.height)
        if by_height and by_height.id != yard.id:
            raise MastYardAlreadyExistsException(by_height.config.name, data.height)

        return await self._update(yard, data)

    async def delete_mast_yard(self, id_: UUID):
        yard = await self.repository.get_by_id(id_)

        await self._delete(yard)
