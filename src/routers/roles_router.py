from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from src.factories import ServiceFactory
from src.schemas import (
    CreateRoleSchema,
    ResponseModel,
    RoleSchema,
    RoleWithPermissionsSchema,
    UpdateRoleSchema,
    RolePermissionSchema,
    AddPermissionToRoleSchema,
    DeletePermissionToRoleSchema,
)
from src.services import RoleService
from src.utils import get_responses

roles_router = APIRouter(prefix="/roles", tags=["Роли пользователей"])


@roles_router.get(
    "/",
    response_model=List[RoleWithPermissionsSchema],
    status_code=200,
    responses=get_responses(),
)
async def get_roles(
    include_deleted: bool = False,
    service: RoleService = Depends(ServiceFactory.get_role_service),
):
    return await service.get_all_with_permissions(include_deleted)


@roles_router.post(
    "/",
    response_model=RoleSchema,
    status_code=201,
    responses=get_responses(
        [ResponseModel(status_code=409, description="Роль уже существует")]
    ),
)
async def create_role(
    data: CreateRoleSchema,
    service: RoleService = Depends(ServiceFactory.get_role_service),
):
    return await service.create_role(data)


@roles_router.get(
    "/{id_}",
    response_model=RoleWithPermissionsSchema,
    status_code=200,
    responses=get_responses(),
)
async def get_role_with_permissions(
    id_: UUID,
    service: RoleService = Depends(ServiceFactory.get_role_service),
):
    return await service.get_role_with_permissions(id_)



@roles_router.post(
    "/{id_}",
    response_model=RoleSchema,
    status_code=200,
    responses=get_responses(
        [
            ResponseModel(status_code=400, description="Роль не удалена"),
            ResponseModel(status_code=404, description="Роль не найдена"),
        ]
    ),
)
async def restore_role(
    id_: UUID, service: RoleService = Depends(ServiceFactory.get_role_service)
):
    return await service.restore_role(id_)


@roles_router.patch(
    "/{id_}",
    response_model=RoleSchema,
    status_code=200,
    responses=get_responses(
        [ResponseModel(status_code=404, description="Роль не найдена"),
         ResponseModel(status_code=409, description="Роль уже существует")]
    ),
)
async def update_role(
    id_: UUID,
    data: UpdateRoleSchema,
    service: RoleService = Depends(ServiceFactory.get_role_service),
):
    return await service.update_role(id_, data)


@roles_router.delete(
    "/{id_}",
    status_code=204,
    responses=get_responses(
        [ResponseModel(status_code=404, description="Роль не найдена"),
         ResponseModel(status_code=409, description="Роль не может быть удалена")]
    ),
)
async def delete_role(
    id_: UUID,
    force: bool = False,
    service: RoleService = Depends(ServiceFactory.get_role_service),
):
    await service.delete_role(id_, force)


@roles_router.post(
    "/{id_}/permissions",
    response_model=List[RolePermissionSchema],
    status_code=201,
    responses=get_responses(
        [
            ResponseModel(status_code=404, description="Роль не найдена"),
            ResponseModel(status_code=404, description="Разрешение не найдено"),
        ]
    ),
)
async def add_permission_to_role(
    id_: UUID,
    data: List[AddPermissionToRoleSchema],
    service: RoleService = Depends(ServiceFactory.get_role_service)
):
    return await service.create_roles_permissions(id_, data)


@roles_router.delete(
    "/{id_}/permissions",
    status_code=204,
    responses=get_responses(
        [
            ResponseModel(status_code=404, description="Роль не найдена"),
            ResponseModel(status_code=404, description="Разрешение не найдено"),
        ]
    ),
)
async def delete_permission_from_role(
    id_: UUID,
    data: List[DeletePermissionToRoleSchema],
    service: RoleService = Depends(ServiceFactory.get_role_service)
):
    return await service.delete_roles_permissions(id_, data)