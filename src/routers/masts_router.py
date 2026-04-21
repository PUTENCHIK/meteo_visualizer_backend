from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from src.auth.callable import PermissionRequired as required
from src.auth.enums import SystemPermission as p
from src.factories import ServiceFactory
from src.models import User
from src.schemas import (
    CreateMastSchema,
    MastSchema,
    ResponseModel,
    UpdateMastSchema,
)
from src.services import MastService
from src.utils import get_responses

masts_router = APIRouter(prefix="/masts", tags=["Мачты комплексов"])


@masts_router.get(
    "/",
    response_model=List[MastSchema],
    status_code=200,
    responses=get_responses(),
)
async def get_masts(
    service: MastService = Depends(ServiceFactory.get_mast_service),
    user: User = Depends(required(p.MAST_READ)),
):
    return await service.get_all()


@masts_router.get(
    "/{id_}",
    response_model=MastSchema,
    status_code=200,
    responses=get_responses(
        [
            ResponseModel(status_code=404, description="Мачта не найдена"),
        ]
    ),
)
async def get_mast(
    id_: UUID,
    service: MastService = Depends(ServiceFactory.get_mast_service),
    user: User = Depends(required(p.MAST_READ)),
):
    return await service.get_by_id(id_)


@masts_router.post(
    "/",
    response_model=MastSchema,
    status_code=201,
    responses=get_responses(
        [
            ResponseModel(status_code=404, description="Комплекс не найден"),
            ResponseModel(status_code=404, description="Конфиг мачты не найден"),
        ]
    ),
)
async def create_mast(
    data: CreateMastSchema,
    service: MastService = Depends(ServiceFactory.get_mast_service),
    user: User = Depends(required(p.MAST_CREATE)),
):
    return await service.create_mast(data)


@masts_router.patch(
    "/{id_}",
    response_model=MastSchema,
    status_code=200,
    responses=get_responses(
        [
            ResponseModel(status_code=404, description="Мачта не найдена"),
            ResponseModel(status_code=404, description="Конфиг мачты не найден"),
        ]
    ),
)
async def update_mast(
    id_: UUID,
    data: UpdateMastSchema,
    service: MastService = Depends(ServiceFactory.get_mast_service),
    user: User = Depends(required(p.MAST_UPDATE)),
):
    return await service.update_mast(id_, data)


@masts_router.delete(
    "/{id_}",
    status_code=204,
    responses=get_responses(
        [
            ResponseModel(status_code=404, description="Мачта не найдена"),
        ]
    ),
)
async def delete_mast(
    id_: UUID,
    service: MastService = Depends(ServiceFactory.get_mast_service),
    user: User = Depends(required(p.MAST_DELETE)),
):
    return await service.delete_mast(id_)
