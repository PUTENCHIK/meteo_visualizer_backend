from fastapi import Depends
from src.utils.permissions.system_permission import SystemPermission
from src.utils import get_current_user
from src.models import User
from src.services import AuthService
from src.factories import ServiceFactory


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
    
    async def __call__(self,
                       user: User = Depends(get_current_user), 
        service: AuthService = Depends(ServiceFactory.get_auth_service)
):
        has_permission = await service.check_user_permission(user.role_id, self.permission_name)
        
        if not has_permission:
            raise HTTPException(
                status_code=403,
                detail=f"Недостаточно прав: требуется {self.permission_name}"
            )
        return user
