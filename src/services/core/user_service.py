from typing import override
from uuid import UUID

from src.models import User
from src.repositories import RoleRepository, UserRepository
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

    __role_repo: RoleRepository

    @property
    def role_repo(self) -> RoleRepository:
        return self.__role_repo

    def __init__(self, repository: UserRepository, role_repo: RoleRepository):
        super().__init__(repository)
        self.__role_repo = role_repo

    @override
    async def get_by_id(self, id_, include_deleted=False) -> User:
        user = await self._repository.get_by_id(id_, include_deleted)
        if not user:
            raise UserNotFoundException(id_)
        return user

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
