from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from src.factories import ServiceFactory
from src.schemas import (
    CreateRoleSchema,
    ResponseModel,
    RoleSchema,
    RoleWithParentSchema,
    UpdateRoleSchema,
)
from src.services import RoleService
from src.utils import default_responses

roles_router = APIRouter(prefix="/roles", tags=["Роли пользователей"])


@roles_router.get(
    "/",
    response_model=List[RoleWithParentSchema],
    status_code=200,
    responses=default_responses(),
)
async def get_roles(
    include_deleted: bool = False,
    service: RoleService = Depends(ServiceFactory.get_role_service),
):
    return await service.get_all(include_deleted)


@roles_router.post(
    "/",
    response_model=RoleSchema,
    status_code=201,
    responses=default_responses(
        [ResponseModel(status_code=409, description="Роль уже существует")]
    ),
)
async def create_role(
    data: CreateRoleSchema,
    service: RoleService = Depends(ServiceFactory.get_role_service),
):
    return await service.create_role(data)


@roles_router.post(
    "/{id_}",
    response_model=RoleSchema,
    status_code=200,
    responses=default_responses(
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
    status_code=201,
    responses=default_responses(
        [ResponseModel(status_code=404, description="Роль не найдена")]
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
    responses=default_responses(
        [ResponseModel(status_code=404, description="Роль не найдена")]
    ),
)
async def delete_role(
    id_: UUID,
    force: bool = False,
    service: RoleService = Depends(ServiceFactory.get_role_service),
):
    await service.delete_role(id_, force)
