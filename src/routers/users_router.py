from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from src.auth.callable import PermissionRequired as required
from src.auth.enums import SystemPermission as p
from src.factories import AuthFactory, ServiceFactory
from src.models import User
from src.schemas import (
    ActiveUserSchema,
    ComplexAccessSchema,
    ResponseModel,
    UpdateUserSchema,
    UserWithRoleSchema,
)
from src.services import UserService
from src.utils import get_responses

users_router = APIRouter(prefix="/users", tags=["Пользователи"])


@users_router.get(
    "/",
    response_model=List[UserWithRoleSchema],
    status_code=200,
    responses=get_responses(),
)
async def get_users(
    include_deleted: bool = False,
    service: UserService = Depends(ServiceFactory.get_user_service),
    user: User = Depends(required(p.USER_READ)),
):
    return await service.get_all(include_deleted)


@users_router.get(
    "/me",
    response_model=ActiveUserSchema,
    status_code=200,
    responses=get_responses(
        [
            ResponseModel(status_code=401, description="Токен доступа заблокирован"),
        ]
    ),
)
async def get_active_user(
    user: User = Depends(AuthFactory.get_current_user),
):
    return user


@users_router.get(
    "/me/complexes",
    response_model=List[ComplexAccessSchema],
    status_code=200,
    responses=get_responses(
        [
            ResponseModel(status_code=401, description="Токен доступа заблокирован"),
        ]
    ),
)
async def get_active_user_complexes(
    service: UserService = Depends(ServiceFactory.get_user_service),
    user: User = Depends(AuthFactory.get_current_user),
):
    return await service.get_user_complexes(user)


@users_router.post(
    "/{id_}",
    response_model=UserWithRoleSchema,
    status_code=200,
    responses=get_responses(
        [
            ResponseModel(status_code=400, description="Пользователь не удалён"),
            ResponseModel(status_code=404, description="Пользователь не найден"),
        ]
    ),
)
async def restore_user(
    id_: UUID,
    service: UserService = Depends(ServiceFactory.get_user_service),
    user: User = Depends(required(p.USER_RESTORE)),
):
    return await service.restore_user(id_)


@users_router.patch(
    "/{id_}",
    response_model=UserWithRoleSchema,
    status_code=200,
    responses=get_responses(
        [
            ResponseModel(status_code=404, description="Пользователь не найден"),
            ResponseModel(status_code=404, description="Роль не найдена"),
        ]
    ),
)
async def update_user(
    id_: UUID,
    data: UpdateUserSchema,
    service: UserService = Depends(ServiceFactory.get_user_service),
    user: User = Depends(required(p.USER_UPDATE)),
):
    return await service.update_user(id_, data)


@users_router.delete(
    "/{id_}",
    status_code=204,
    responses=get_responses(
        [
            ResponseModel(status_code=404, description="Пользователь не найден"),
        ]
    ),
)
async def delete_user(
    id_: UUID,
    force: bool = False,
    service: UserService = Depends(ServiceFactory.get_user_service),
    user: User = Depends(required(p.USER_DELETE)),
):
    return await service.delete_user(id_, force)
