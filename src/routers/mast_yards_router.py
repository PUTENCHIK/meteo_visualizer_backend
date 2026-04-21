from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from src.auth.callable import PermissionRequired as required
from src.auth.enums import SystemPermission as p
from src.factories import ServiceFactory
from src.models import User
from src.schemas import (
    CreateMastYardSchema,
    MastYardSchema,
    ResponseModel,
    UpdateMastYardSchema,
)
from src.services import MastYardService
from src.utils import get_responses

mast_yards_router = APIRouter(prefix="/mast-yards", tags=["Реи мачт"])


@mast_yards_router.get(
    "/",
    response_model=List[MastYardSchema],
    status_code=200,
    responses=get_responses(),
)
async def get_mast_yards(
    service: MastYardService = Depends(ServiceFactory.get_mast_yard_service),
    user: User = Depends(required(p.MAST_YARD_READ)),
):
    return await service.get_all()


@mast_yards_router.get(
    "/{id_}",
    response_model=MastYardSchema,
    status_code=200,
    responses=get_responses(
        [
            ResponseModel(status_code=404, description="Рея не найдена"),
        ]
    ),
)
async def get_mast_yard(
    id_: UUID,
    service: MastYardService = Depends(ServiceFactory.get_mast_yard_service),
    user: User = Depends(required(p.MAST_YARD_READ)),
):
    return await service.get_by_id(id_)


@mast_yards_router.post(
    "/",
    response_model=MastYardSchema,
    status_code=201,
    responses=get_responses(
        [
            ResponseModel(status_code=400, description="Неверная высота"),
            ResponseModel(status_code=404, description="Конфиг не найден"),
            ResponseModel(status_code=409, description="Рея уже существует"),
        ]
    ),
)
async def create_mast_yard(
    data: CreateMastYardSchema,
    service: MastYardService = Depends(ServiceFactory.get_mast_yard_service),
    user: User = Depends(required(p.MAST_YARD_CREATE)),
):
    return await service.create_mast_yard(data)


@mast_yards_router.patch(
    "/{id_}",
    response_model=MastYardSchema,
    status_code=200,
    responses=get_responses(
        [
            ResponseModel(status_code=400, description="Неверная высота"),
            ResponseModel(status_code=404, description="Рея не найдена"),
            ResponseModel(status_code=409, description="Рея уже существует"),
        ]
    ),
)
async def update_mast_yard(
    id_: UUID,
    data: UpdateMastYardSchema,
    service: MastYardService = Depends(ServiceFactory.get_mast_yard_service),
    user: User = Depends(required(p.MAST_YARD_UPDATE)),
):
    return await service.update_mast_yard(id_, data)


@mast_yards_router.delete(
    "/{id_}",
    status_code=204,
    responses=get_responses(
        [ResponseModel(status_code=404, description="Рея не найдена")]
    ),
)
async def delete_mast_yard(
    id_: UUID,
    service: MastYardService = Depends(ServiceFactory.get_mast_yard_service),
    user: User = Depends(required(p.MAST_YARD_DELETE)),
):
    return await service.delete_mast_yard(id_)
