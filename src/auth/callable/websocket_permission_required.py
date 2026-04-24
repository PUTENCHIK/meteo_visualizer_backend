from typing import Optional
from fastapi import Depends, Query, WebSocket, WebSocketException

from src.auth.enums import SystemPermission
from src.factories import AuthFactory, ServiceFactory
from src.models import User
from src.services import AuthService, UserService
from src.utils.exceptions import TokenBlockedException, TokenExpiredException


class WebsocketPermissionRequired:
    """
    Callable-класс для проверки прав пользователя с помощью отправленного в параметрах
    токена доступа
    """

    __value: SystemPermission

    @property
    def value(self) -> SystemPermission:
        return self.__value

    def __init__(self, permission: SystemPermission):
        self.__value = permission

    async def __call__(
        self,
        websocket: WebSocket, 
        token: Optional[str] = Query(None, alias="token"),
        auth_service: AuthService = Depends(ServiceFactory.get_auth_service),
        user_service: UserService = Depends(ServiceFactory.get_user_service),
    ) -> User:
        await websocket.accept()

        try:
            user = await AuthFactory.get_query_user(user_service, token)
            await auth_service.has_permission(user, self.value)
            return user
        except (TokenBlockedException, TokenExpiredException) as e:
            raise WebSocketException(code=4001, reason=str(e))
        except Exception as e:
            raise WebSocketException(code=1008, reason=str(e))

