from uuid import UUID

from src.models import Role
from src.repositories import RoleRepository
from src.schemas import CreateRoleSchema, UpdateRoleSchema
from src.services.abstractions.auditable_service import AuditableService
from src.utils.exceptions import (
    RoleNameAlreadyExistsException,
    RoleNotDeletedException,
    RoleNotFoundException,
    RoleParentCantBeSameException,
)


class RoleService(AuditableService[Role, RoleRepository]):
    """
    Сервис ролей пользователей
    """

    def __init__(self, repository: RoleRepository):
        super().__init__(repository)

    async def create_role(self, data: CreateRoleSchema) -> Role:
        role = await self._repository.get_by_name(data.name)
        if role:
            raise RoleNameAlreadyExistsException(data.name)

        new_role = Role(
            name=data.name,
            parent_id=data.parent_id,
        )

        return await self._repository.add(new_role)

    async def restore_role(self, id_: UUID) -> Role:
        role = await self._repository.get_by_id(id_, include_deleted=True)
        if not role:
            raise RoleNotFoundException(id_)

        if role.deleted_at is None:
            raise RoleNotDeletedException(id_)

        return await self.repository.restore(role)

    async def update_role(self, id_: UUID, data: UpdateRoleSchema) -> Role:
        role = await self._repository.get_by_id(id_)
        if not role:
            raise RoleNotFoundException(id_)

        if data.parent_id == id_:
            raise RoleParentCantBeSameException()

        return await self._repository.update(role, data)

    async def delete_role(self, id_: UUID, force: bool = False):
        role = await self._repository.get_by_id(id_)
        if not role:
            raise RoleNotFoundException(id_)

        await self._repository.delete(role, force)
