from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from src.auth.callable import PermissionRequired as PermissionRequired
from src.auth.enums import SystemPermission as p
from src.factories.service import ServiceFactory
from src.models import User
from src.schemas import (
    CreateMeasureAliasSchema,
    MeasureAliasSchema,
    ResponseModel,
    UpdateMeasureAliasSchema,
)
from src.services import MeasureAliasService
from src.utils import get_responses

measure_aliases_router = APIRouter(
    prefix="/measure-aliases", tags=["Псевдонимы пользовательских параметров"]
)


@measure_aliases_router.get(
    "/",
    response_model=List[MeasureAliasSchema],
    status_code=200,
    responses=get_responses(),
)
async def get_measure_aliases(
    service: MeasureAliasService = Depends(ServiceFactory.get_measure_alias_service),
    user: User = Depends(PermissionRequired(p.MEASURE_ALIAS_READ)),
):
    return await service.get_all()


@measure_aliases_router.get(
    "/{id_}",
    response_model=MeasureAliasSchema,
    status_code=200,
    responses=get_responses(
        [
            ResponseModel(status_code=404, description="Псевдоним не найден"),
        ]
    ),
)
async def get_measure_alias(
    id_: UUID,
    service: MeasureAliasService = Depends(ServiceFactory.get_measure_alias_service),
    user: User = Depends(PermissionRequired(p.MEASURE_ALIAS_READ)),
):
    return await service.get_by_id(id_)


@measure_aliases_router.post(
    "/",
    response_model=MeasureAliasSchema,
    status_code=201,
    responses=get_responses(
        [
            ResponseModel(status_code=404, description="Псевдоним не найден"),
        ]
    ),
)
async def create_measure_alias(
    data: CreateMeasureAliasSchema,
    service: MeasureAliasService = Depends(ServiceFactory.get_measure_alias_service),
    user: User = Depends(PermissionRequired(p.MEASURE_ALIAS_CREATE)),
):
    return await service.create_measure_alias(data)


@measure_aliases_router.patch(
    "/{id_}",
    response_model=MeasureAliasSchema,
    status_code=200,
    responses=get_responses(
        [
            ResponseModel(status_code=404, description="Псевдоним не найден"),
        ]
    ),
)
async def update_measure_alias(
    id_: UUID,
    data: UpdateMeasureAliasSchema,
    service: MeasureAliasService = Depends(ServiceFactory.get_measure_alias_service),
    user: User = Depends(PermissionRequired(p.MEASURE_ALIAS_UPDATE)),
):
    return await service.update_measure_alias(id_, data)


@measure_aliases_router.delete(
    "/{id_}",
    status_code=204,
    responses=get_responses(
        [ResponseModel(status_code=404, description="Псевдоним не найден"),]
    ),
)
async def delete_measure_alias(
    id_: UUID,
    service: MeasureAliasService = Depends(ServiceFactory.get_measure_alias_service),
    user: User = Depends(PermissionRequired(p.MEASURE_ALIAS_DELETE)),
):
    return await service.delete_measure_alias(id_)

