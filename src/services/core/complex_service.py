from typing import override
from uuid import UUID

from sqlmodel.ext.asyncio.session import AsyncSession

from src.managers import PasswordManager
from src.models import Complex, User
from src.repositories import ComplexRepository
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

    _password_manager: PasswordManager = PasswordManager()

    @property
    def password_manager(self) -> PasswordManager:
        return self._password_manager

    def __init__(self, session: AsyncSession):
        super().__init__(ComplexRepository(session))

    @override
    async def get_by_id(self, id_, include_deleted=False) -> Complex:
        complex = await self.repository.get_by_id(id_, include_deleted)
        if not complex:
            raise ComplexNotFoundException(id_)
        return complex

    async def create_complex(self, data: CreateComplexSchema, user: User) -> Complex:
        password_hash = (
            self.password_manager.hash_password(data.password)
            if data.password
            else None
        )

        new_complex = Complex(
            **data.model_dump(exclude={"password"}),
            password_hash=password_hash,
            creator_id=user.id,
        )
        new_complex = await self._create(new_complex)

        return await self.get_by_id(new_complex.id)

    async def restore_complex(self, id_: UUID) -> Complex:
        complex = await self.get_by_id(id_, include_deleted=True)

        if complex.deleted_at is None:
            raise ComplexNotDeletedException(id_)

        return await self._restore(complex)

    async def update_complex(self, id_: UUID, data: UpdateComplexSchema) -> Complex:
        complex = await self.get_by_id(id_)

        json_data = data.model_dump(exclude_unset=True)

        if "password" in json_data:
            raw_password = json_data.pop("password")
            complex.password_hash = (
                self.password_manager.hash_password(raw_password)
                if raw_password
                else None
            )

        return await self._update(complex, data)

    async def delete_complex(self, id_: UUID, force: bool = False):
        complex = await self.get_by_id(id_)

        # TODO: удалять связанные мачты

        return await self._delete(complex, force)
