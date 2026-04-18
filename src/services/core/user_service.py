from typing import List, override
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import ComplexUser, User
from src.repositories import ComplexUserRepository, RoleRepository, UserRepository
from src.schemas import UpdateUserSchema
from src.services.abstractions.auditable_service import AuditableService
from src.utils.exceptions import (
    RoleNotFoundException,
    UserNotDeletedException,
    UserNotFoundException,
)


class UserService(AuditableService[User, UserRepository]):
    """
    Сервис пользователей
    """

    _role_repo: RoleRepository
    _comp_user_repo: ComplexUserRepository

    @property
    def role_repo(self) -> RoleRepository:
        return self._role_repo

    @property
    def comp_user_repo(self) -> ComplexUserRepository:
        return self._comp_user_repo

    def __init__(
        self,
        session: AsyncSession
    ):
        super().__init__(UserRepository(session))
        self._role_repo = RoleRepository(session)
        self._comp_user_repo = ComplexUserRepository(session)

    @override
    async def get_by_id(self, id_, include_deleted=False) -> User:
        user = await self.repository.get_by_id(id_, include_deleted)
        if not user:
            raise UserNotFoundException(id_)
        return user

    async def get_user_complexes(self, user: User) -> List[ComplexUser]:
        links = await self.comp_user_repo.get_by_user(user.id)

        return sorted(links, key=lambda x: x.complex.updated_at, reverse=True)

    async def restore_user(self, id_: UUID) -> User:
        user = await self.get_by_id(id_, include_deleted=True)

        if user.deleted_at is None:
            raise UserNotDeletedException(id_)

        user = await self._restore(user)
        await self.repository.commit_refresh(user)

        return user

    async def update_user(self, id_: UUID, data: UpdateUserSchema) -> User:
        user = await self.get_by_id(id_)

        if data.role_id is not None:
            role = await self.role_repo.get_by_id(data.role_id)
            if not role:
                raise RoleNotFoundException(data.role_id)

        user = await self.repository.update(user, data)
        await self.repository.commit_refresh(user)

        return user

    async def delete_user(self, id_: UUID, force: bool = False):
        user = await self.get_by_id(id_)

        # TODO: проверка на связанные комплексы и меры

        await self._delete(user, force)
