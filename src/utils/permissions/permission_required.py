from fastapi import Depends

from src.factories import AuthFactory, ServiceFactory
from src.models import User
from src.services import AuthService
from src.utils.permissions.system_permission import SystemPermission


class PermissionRequired:
    """
    Сущность зависимости
    """

    __value: SystemPermission

    @property
    def value(self) -> SystemPermission:
        return self.__value

    def __init__(self, permission: SystemPermission):
        self.__value = permission

    async def __call__(
        self,
        user: User = Depends(AuthFactory.get_current_user),
        service: AuthService = Depends(ServiceFactory.get_auth_service),
    ):
        pass
        # has_permission =
        # await service.check_user_permission(user.role_id, self.permission_name)

        # if not has_permission:
        #     raise HTTPException(
        #         status_code=403,
        #         detail=f"Недостаточно прав: требуется {self.permission_name}"
        #     )
        # return user
