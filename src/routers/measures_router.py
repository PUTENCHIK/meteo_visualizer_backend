from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from src.auth.callable import PermissionRequired
from src.auth.enums import SystemPermission as p
from src.factories.service import ServiceFactory
from src.models import User
from src.schemas import (
    CreateMeasureSchema,
    MeasureWithDependentsSchema,
    ResponseModel,
    UpdateMeasureSchema,
)
from src.services import AuthService, MeasureService
from src.utils import get_responses

measures_router = APIRouter(prefix="/measures", tags=["Пользовательские параметры"])


@measures_router.get(
    "/",
    response_model=List[MeasureWithDependentsSchema],
    status_code=200,
    responses=get_responses(),
)
async def get_measures(
    include_deleted: bool = False,
    service: MeasureService = Depends(ServiceFactory.get_measure_service),
    auth_service: AuthService = Depends(ServiceFactory.get_auth_service),
    user: User = Depends(PermissionRequired(p.MEASURE_READ)),
):
    return await service.get_all(
        include_deleted and await auth_service.has_permission(user, p.MEASURE_RESTORE)
    )


@measures_router.get(
    "/{id_}",
    response_model=MeasureWithDependentsSchema,
    status_code=200,
    responses=get_responses(
        [
            ResponseModel(status_code=404, description="Параметр не найден"),
        ]
    ),
)
async def get_measure(
    id_: UUID,
    include_deleted: bool = False,
    service: MeasureService = Depends(ServiceFactory.get_measure_service),
    user: User = Depends(PermissionRequired(p.COMPLEX_READ)),
):
    return await service.get_by_id(id_, include_deleted)


@measures_router.post(
    "/",
    response_model=MeasureWithDependentsSchema,
    status_code=201,
    responses=get_responses([
        ResponseModel(status_code=400, description="Минимум больше максимума"),
    ]),
)
async def create_measure(
    data: CreateMeasureSchema,
    service: MeasureService = Depends(ServiceFactory.get_measure_service),
    user: User = Depends(PermissionRequired(p.MEASURE_CREATE)),
):
    return await service.create_measure(data, user)


@measures_router.post(
    "/{id_}",
    status_code=200,
    response_model=MeasureWithDependentsSchema,
    responses=get_responses(
        [
            ResponseModel(status_code=400, description="Параметр не удалён"),
            ResponseModel(status_code=404, description="Параметр не найден"),
        ]
    ),
)
async def restore_measure(
    id_: UUID,
    service: MeasureService = Depends(ServiceFactory.get_measure_service),
    user: User = Depends(PermissionRequired(p.MEASURE_RESTORE)),
):
    return await service.restore_measure(id_)


@measures_router.patch(
    "/{id_}",
    response_model=MeasureWithDependentsSchema,
    status_code=200,
    responses=get_responses(
        [
            ResponseModel(status_code=400, description="Минимум больше максимума"),
            ResponseModel(status_code=404, description="Параметр не найден"),
        ]
    ),
)
async def update_measure(
    id_: UUID,
    data: UpdateMeasureSchema,
    service: MeasureService = Depends(ServiceFactory.get_measure_service),
    user: User = Depends(PermissionRequired(p.MEASURE_UPDATE)),
):
    return await service.update_measure(id_, data)


@measures_router.delete(
    "/{id_}",
    status_code=204,
    responses=get_responses(
        [
            ResponseModel(status_code=404, description="Параметр не найден"),
        ]
    ),
)
async def delete_measure(
    id_: UUID,
    force: bool = False,
    service: MeasureService = Depends(ServiceFactory.get_measure_service),
    user: User = Depends(PermissionRequired(p.MEASURE_DELETE)),
):
    return await service.delete_measure(id_, force)
