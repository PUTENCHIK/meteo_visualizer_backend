from uuid import UUID
from typing import override
from src.models import Permission
from src.repositories import PermissionRepository
from src.schemas import CreatePermissionSchema, UpdatePermissionSchema
from src.services.abstractions.auditable_service import AuditableService
from src.utils.exceptions import (
    PermissionNameAlreadyExistsException,
    PermissionNotFoundException,
    PermissionNotDeletedException
)


class PermissionService(AuditableService[Permission, PermissionRepository]):
    """
    Сервис разрешений для ролей пользователей
    """

    def __init__(self, repository: PermissionRepository):
        super().__init__(repository)

    @override
    async def get_by_id(self, id_, include_deleted = False) -> Permission:
        permission = await self._repository.get_by_id(id_, include_deleted)
        if not permission:
            raise PermissionNotFoundException(id_)
        return permission
    
    async def create_permission(self, data: CreatePermissionSchema) -> Permission:
        permission = await self._repository.get_by_name(data.name, include_deleted=True)
        if permission:
            if permission.deleted_at is None:
                raise PermissionNameAlreadyExistsException(data.name)
            else:
                permission = await self.restore_permission(permission.id)
                return await self.update_permission(permission.id,
                                                UpdatePermissionSchema(
                    description=data.description
                ))

        new_perm = Permission(
            name=data.name,
            description=data.description
        )

        return await self._create(new_perm)
    
    async def restore_permission(self, id_: UUID) -> Permission:
        permission = await self.get_by_id(id_, include_deleted=True)

        if permission.deleted_at is None:
            raise PermissionNotDeletedException(id_)

        return await self._restore(permission)
    
    async def update_permission(
            self, id_: UUID, data: UpdatePermissionSchema) -> Permission:
        permission = await self.get_by_id(id_)

        return await self._repository.update(permission, data)

    async def delete_permission(self, id_: UUID, force: bool = False):
        permission = await self.get_by_id(id_)

        await self._delete(permission, force)