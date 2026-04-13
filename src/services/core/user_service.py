from typing import override

from src.models import User
from src.repositories import UserRepository
from src.services.abstractions.auditable_service import AuditableService
from src.utils.exceptions import UserNotFoundException


class UserService(AuditableService[User, UserRepository]):
    """
    Сервис пользователей
    """

    def __init__(self, repository: UserRepository):
        super().__init__(repository)

    @override
    async def get_by_id(self, id_, include_deleted=False) -> User:
        user = await self._repository.get_by_id(id_, include_deleted)
        if not user:
            raise UserNotFoundException(id_)
        return user
