from typing import override
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import Complex, User
from src.repositories import ComplexRepository, MastRepository
from src.schemas import CreateComplexSchema, UpdateComplexSchema
from src.services.abstractions.auditable_service import AuditableService
from src.utils.exceptions import (
    ComplexNotDeletedException,
    ComplexNotFoundException,
)


class ComplexService(AuditableService[Complex, ComplexRepository]):
    """
    Сервис комплексов
    """

    _mast_repo: MastRepository

    @property
    def mast_repo(self) -> MastRepository:
        return self._mast_repo

    def __init__(self, session: AsyncSession):
        super().__init__(ComplexRepository(session))
        self._mast_repo = MastRepository(session)

    @override
    async def get_by_id(self, id_, include_deleted=False) -> Complex:
        complex = await self.repository.get_by_id(id_, include_deleted)
        if not complex:
            raise ComplexNotFoundException(id_)
        return complex

    async def create_complex(self, data: CreateComplexSchema, user: User) -> Complex:
        new_complex = Complex(
            **data.model_dump(),
            creator_id=user.id,
        )
        new_complex = await self._create(new_complex)

        return await self.get_by_id(new_complex.id)

    async def restore_complex(self, id_: UUID) -> Complex:
        complex = await self.get_by_id(id_, include_deleted=True)

        if complex.deleted_at is None:
            raise ComplexNotDeletedException(id_)

        masts = await self.mast_repo.get_by_complex(id_, include_deleted=True)
        for mast in masts:
            print(mast.id, mast.deleted_at)
            await self.mast_repo.restore(mast)

        return await self._restore(complex)

    async def update_complex(self, id_: UUID, data: UpdateComplexSchema) -> Complex:
        complex = await self.get_by_id(id_)

        return await self._update(complex, data)

    async def delete_complex(self, id_: UUID, force: bool = False):
        complex = await self.get_by_id(id_)

        for mast in complex.masts:
            await self.mast_repo.delete(mast, force)

        return await self._delete(complex, force)
