from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from src.auth.callable import PermissionRequired as required
from src.auth.enums import SystemPermission as p
from src.factories import ServiceFactory
from src.models import User
from src.schemas import (
    CreateMastConfigSchema,
    MastConfigSchema,
    ResponseModel,
    UpdateMastConfigSchema,
)
from src.services import MastConfigService
from src.utils import get_responses

mast_configs_router = APIRouter(prefix="/mast-configs", tags=["Конфиги мачт"])


@mast_configs_router.get(
    "/",
    response_model=List[MastConfigSchema],
    status_code=200,
    responses=get_responses(),
)
async def get_mast_configs(
    include_deleted: bool = False,
    service: MastConfigService = Depends(ServiceFactory.get_mast_config_service),
    user: User = Depends(required(p.MAST_CONFIG_READ)),
):
    return await service.get_all(include_deleted)


@mast_configs_router.post(
    "/",
    response_model=MastConfigSchema,
    status_code=201,
    responses=get_responses(),
)
async def create_mast_config(
    data: CreateMastConfigSchema,
    service: MastConfigService = Depends(ServiceFactory.get_mast_config_service),
    user: User = Depends(required(p.MAST_CONFIG_CREATE)),
):
    return await service.create_mast_config(data)


@mast_configs_router.post(
    "/{id_}",
    response_model=MastConfigSchema,
    status_code=200,
    responses=get_responses(
        [
            ResponseModel(status_code=400, description="Конфиг не удалён"),
            ResponseModel(status_code=404, description="Конфиг не найден"),
        ]
    ),
)
async def restore_mast_config(
    id_: UUID,
    service: MastConfigService = Depends(ServiceFactory.get_mast_config_service),
    user: User = Depends(required(p.MAST_CONFIG_RESTORE)),
):
    return await service.restore_mast_config(id_)


@mast_configs_router.patch(
    "/{id_}",
    response_model=MastConfigSchema,
    status_code=200,
    responses=get_responses(
        [
            ResponseModel(status_code=404, description="Конфиг не найден"),
        ]
    ),
)
async def update_mast_config(
    id_: UUID,
    data: UpdateMastConfigSchema,
    service: MastConfigService = Depends(ServiceFactory.get_mast_config_service),
    user: User = Depends(required(p.MAST_CONFIG_UPDATE)),
):
    return await service.update_mast_config(id_, data)


@mast_configs_router.delete(
    "/{id_}",
    status_code=204,
    responses=get_responses(
        [
            ResponseModel(status_code=404, description="Конфиг не найден"),
        ]
    ),
)
async def delete_mast_config(
    id_: UUID,
    force: bool = False,
    service: MastConfigService = Depends(ServiceFactory.get_mast_config_service),
    user: User = Depends(required(p.MAST_CONFIG_DELETE)),
):
    return await service.delete_mast_config(id_, force)
