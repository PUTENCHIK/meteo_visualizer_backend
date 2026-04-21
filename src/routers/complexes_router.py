from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from src.auth.callable import PermissionRequired as required
from src.auth.enums import SystemPermission as p
from src.factories import ServiceFactory
from src.models import User
from src.schemas import (
    ComplexFavoriteSchema,
    ComplexWithFavoriteInfoSchema,
    ComplexWithMastsSchema,
    CreateComplexSchema,
    ResponseModel,
    UpdateComplexSchema,
)
from src.services import ComplexService
from src.utils import get_responses

complexes_router = APIRouter(prefix="/complexes", tags=["Комплексы"])


@complexes_router.get(
    "/",
    response_model=List[ComplexWithFavoriteInfoSchema],
    response_model_exclude_unset=True,
    status_code=200,
    responses=get_responses(),
)
async def get_complexes(
    include_deleted: bool = False,
    service: ComplexService = Depends(ServiceFactory.get_complex_service),
    user: User = Depends(required(p.COMPLEX_READ)),
):
    return await service.get_all_with_favorite(user, include_deleted)


@complexes_router.get(
    "/{id_}",
    response_model=ComplexWithFavoriteInfoSchema,
    response_model_exclude_unset=True,
    status_code=200,
    responses=get_responses(
        [
            ResponseModel(status_code=404, description="Комплекс не найден"),
        ]
    ),
)
async def get_complex(
    id_: UUID,
    include_deleted: bool = False,
    service: ComplexService = Depends(ServiceFactory.get_complex_service),
    user: User = Depends(required(p.COMPLEX_READ)),
):
    return await service.get_by_id_with_favorite(id_, user, include_deleted)


@complexes_router.post(
    "/",
    response_model=ComplexWithMastsSchema,
    status_code=201,
    responses=get_responses(),
)
async def create_complex(
    data: CreateComplexSchema,
    service: ComplexService = Depends(ServiceFactory.get_complex_service),
    user: User = Depends(required(p.COMPLEX_CREATE)),
):
    return await service.create_complex(data, user)


@complexes_router.post(
    "/{id_}",
    status_code=200,
    response_model=ComplexWithMastsSchema,
    responses=get_responses(
        [
            ResponseModel(status_code=400, description="Комплекс не удалён"),
            ResponseModel(status_code=404, description="Комплекс не найден"),
        ]
    ),
)
async def restore_complex(
    id_: UUID,
    service: ComplexService = Depends(ServiceFactory.get_complex_service),
    user: User = Depends(required(p.COMPLEX_RESTORE)),
):
    return await service.restore_complex(id_)


@complexes_router.patch(
    "/{id_}",
    response_model=ComplexWithMastsSchema,
    status_code=200,
    responses=get_responses(
        [
            ResponseModel(status_code=404, description="Комплекс не найден"),
        ]
    ),
)
async def update_complex(
    id_: UUID,
    data: UpdateComplexSchema,
    service: ComplexService = Depends(ServiceFactory.get_complex_service),
    user: User = Depends(required(p.COMPLEX_UPDATE)),
):
    return await service.update_complex(id_, data)


@complexes_router.delete(
    "/{id_}",
    status_code=204,
    responses=get_responses(
        [
            ResponseModel(status_code=404, description="Комплекс не найден"),
        ]
    ),
)
async def delete_complex(
    id_: UUID,
    force: bool = False,
    service: ComplexService = Depends(ServiceFactory.get_complex_service),
    user: User = Depends(required(p.COMPLEX_DELETE)),
):
    return await service.delete_complex(id_, force)


@complexes_router.post(
    "/{id_}/favorite",
    response_model=ComplexFavoriteSchema,
    status_code=201,
    responses=get_responses(
        [
            ResponseModel(status_code=404, description="Комплекс не найден"),
        ]
    ),
)
async def add_complex_to_user_favorites(
    id_: UUID,
    service: ComplexService = Depends(ServiceFactory.get_complex_service),
    user: User = Depends(required(p.COMPLEX_FAVORITE_CREATE)),
):
    return await service.create_complex_favorite(id_, user.id)


@complexes_router.delete(
    "/{id_}/favorite",
    status_code=204,
    responses=get_responses(
        [
            ResponseModel(status_code=404, description="Комплекс не найден"),
        ]
    ),
)
async def delete_complex_from_user_favorites(
    id_: UUID,
    service: ComplexService = Depends(ServiceFactory.get_complex_service),
    user: User = Depends(required(p.COMPLEX_FAVORITE_DELETE)),
):
    return await service.delete_complex_favorite(id_, user.id)
