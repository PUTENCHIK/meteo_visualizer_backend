from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from src.auth.callable import PermissionRequired as PermissionRequired
from src.auth.enums import SystemPermission as p
from src.factories.service import ServiceFactory
from src.models import User
from src.schemas import (
    CreateMeasureColorSchema,
    MeasureColorSchema,
    ResponseModel,
    UpdateMeasureColorSchema,
)
from src.services import MeasureColorService
from src.utils import get_responses

measure_colors_router = APIRouter(
    prefix="/measure-colors",
    tags=["Цвета пользовательских параметров"]
)


@measure_colors_router.get(
    "/",
    response_model=List[MeasureColorSchema],
    status_code=200,
    responses=get_responses(),
)
async def get_measure_colors(
    service: MeasureColorService = Depends(ServiceFactory.get_measure_color_service),
    user: User = Depends(PermissionRequired(p.MEASURE_COLOR_READ)),
):
    return await service.get_all()


@measure_colors_router.get(
    "/{id_}",
    response_model=MeasureColorSchema,
    status_code=200,
    responses=get_responses(
        [
            ResponseModel(status_code=404, description="Цвет не найден"),
        ]
    ),
)
async def get_measure_color(
    id_: UUID,
    service: MeasureColorService = Depends(ServiceFactory.get_measure_color_service),
    user: User = Depends(PermissionRequired(p.MEASURE_COLOR_READ)),
):
    return await service.get_by_id(id_)


@measure_colors_router.post(
    "/",
    response_model=MeasureColorSchema,
    status_code=201,
    responses=get_responses(
        [
            ResponseModel(status_code=400, description="Похожий цвет уже существует"),
            ResponseModel(status_code=404, description="Цвет не найден"),
            ResponseModel(status_code=404, description="Параметр не найден"),
        ]
    ),
)
async def create_measure_color(
    data: CreateMeasureColorSchema,
    service: MeasureColorService = Depends(ServiceFactory.get_measure_color_service),
    user: User = Depends(PermissionRequired(p.MEASURE_COLOR_CREATE)),
):
    return await service.create_measure_color(data)


@measure_colors_router.patch(
    "/{id_}",
    response_model=MeasureColorSchema,
    status_code=200,
    responses=get_responses(
        [
            ResponseModel(status_code=400, description="Похожий цвет уже существует"),
            ResponseModel(status_code=404, description="Цвет не найден"),
        ]
    ),
)
async def update_measure_color(
    id_: UUID,
    data: UpdateMeasureColorSchema,
    service: MeasureColorService = Depends(ServiceFactory.get_measure_color_service),
    user: User = Depends(PermissionRequired(p.MEASURE_COLOR_UPDATE)),
):
    return await service.update_measure_color(id_, data)


@measure_colors_router.delete(
    "/{id_}",
    status_code=204,
    responses=get_responses(
        [ResponseModel(status_code=404, description="Цвет не найден"),]
    ),
)
async def delete_measure_color(
    id_: UUID,
    service: MeasureColorService = Depends(ServiceFactory.get_measure_color_service),
    user: User = Depends(PermissionRequired(p.MEASURE_COLOR_DELETE)),
):
    return await service.delete_measure_color(id_)
