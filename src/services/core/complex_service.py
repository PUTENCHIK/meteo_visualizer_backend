from typing import List, override
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import Complex, ComplexFavorite, User
from src.repositories import (
    ComplexFavoriteRepository,
    ComplexRepository,
    MastRepository,
)
from src.schemas import (
    ComplexWithFavoriteInfoSchema,
    CreateComplexSchema,
    UpdateComplexSchema,
)
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
    _complex_favorite_repo: ComplexFavoriteRepository

    @property
    def mast_repo(self) -> MastRepository:
        return self._mast_repo

    @property
    def complex_favorite_repo(self) -> ComplexFavoriteRepository:
        return self._complex_favorite_repo

    def __init__(self, session: AsyncSession):
        super().__init__(ComplexRepository(session))
        self._mast_repo = MastRepository(session)
        self._complex_favorite_repo = ComplexFavoriteRepository(session)

    @override
    async def get_by_id(self, id_, include_deleted=False) -> Complex:
        complex = await self.repository.get_by_id(id_, include_deleted)
        if not complex:
            raise ComplexNotFoundException(id_)
        return complex

    async def get_all_with_favorite(
        self, user: User, include_deleted: bool = False
    ) -> List[ComplexWithFavoriteInfoSchema]:
        complexes = await self.repository.get_all(include_deleted)

        favorite_ids = await self.complex_favorite_repo.get_favorites_of_user(
            user_id=user.id, complex_ids=[c.id for c in complexes]
        )
        ids_set = set(favorite_ids)

        schemas = list()
        for complex in complexes:
            schema = ComplexWithFavoriteInfoSchema.model_validate(complex)
            schema.is_favorite = complex.id in ids_set
            schemas.append(schema)
        return schemas

    async def get_by_id_with_favorite(
        self, id_: UUID, user: User, include_deleted: bool = False
    ) -> ComplexWithFavoriteInfoSchema:
        complex = await self.get_by_id(id_, include_deleted)
        link = await self.complex_favorite_repo.get_by_ids(id_, user.id)

        schema = ComplexWithFavoriteInfoSchema.model_validate(complex)
        schema.is_favorite = link is not None

        return schema

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
            await self.mast_repo.restore(mast)

        return await self._restore(complex)

    async def update_complex(self, id_: UUID, data: UpdateComplexSchema) -> Complex:
        complex = await self.get_by_id(id_)
        await self._update(complex, data)

        return await self.get_by_id(id_)

    async def delete_complex(self, id_: UUID, force: bool = False):
        complex = await self.get_by_id(id_)

        for mast in complex.masts:
            await self.mast_repo.delete(mast, force)

        return await self._delete(complex, force)

    async def create_complex_favorite(
        self, id_: UUID, user_id: UUID
    ) -> ComplexFavorite:
        await self.get_by_id(id_)
        link = await self.complex_favorite_repo.get_by_ids(id_, user_id)
        if not link:
            link = ComplexFavorite(
                complex_id=id_,
                user_id=user_id,
                creator_id=user_id,
            )
            await self.complex_favorite_repo.add(link)
            await self.complex_favorite_repo.commit()

        return await self.complex_favorite_repo.get_by_ids(id_, user_id)

    async def delete_complex_favorite(self, id_: UUID, user_id: UUID):
        await self.get_by_id(id_)
        link = await self.complex_favorite_repo.get_by_ids(id_, user_id)
        if link:
            await self.complex_favorite_repo.delete(link)
            await self.complex_favorite_repo.commit()
