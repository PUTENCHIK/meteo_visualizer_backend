from fastapi import Depends

from src.auth.enums import SystemPermission
from src.factories import AuthFactory, ServiceFactory
from src.models import User
from src.services import AuthService


class PermissionRequired:
    """
    Callable-класс для проверки прав пользователя
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
    ) -> User:
        await service.has_permission(user, self.value)
        return user
