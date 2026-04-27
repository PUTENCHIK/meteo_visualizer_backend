from typing import Union

from fastapi import Depends

from src.auth.enums import SystemPermission
from src.auth.requirements import RequirementGroup
from src.factories.auth import AuthFactory
from src.factories.service import ServiceFactory
from src.models import User
from src.services import AuthService


class PermissionRequired:
    """
    Callable-класс для проверки прав пользователя
    """

    __requirement: Union[SystemPermission, RequirementGroup]

    @property
    def requirement(self) -> Union[SystemPermission, RequirementGroup]:
        return self.__requirement

    def __init__(self, requirement: Union[SystemPermission, RequirementGroup]):
        self.__requirement = requirement

    async def __call__(
        self,
        user: User = Depends(AuthFactory.get_current_user),
        service: AuthService = Depends(ServiceFactory.get_auth_service),
    ) -> User:
        await service.is_allowed(user, self.requirement)
        return user
