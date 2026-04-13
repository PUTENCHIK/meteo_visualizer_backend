from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from src.factories import ServiceFactory
from src.schemas import PermissionSchema, ResponseModel, UpdatePermissionSchema
from src.services import PermissionService
from src.utils import get_responses

permission_router = APIRouter(prefix="/permissions", tags=["Разрешения ролей"])


@permission_router.get(
    "/",
    response_model=List[PermissionSchema],
    status_code=200,
    responses=get_responses(),
)
async def get_permissions(
    include_deleted: bool = False,
    service: PermissionService = Depends(ServiceFactory.get_permission_service),
):
    return await service.get_all(include_deleted)


@permission_router.patch(
    "/{id_}",
    response_model=PermissionSchema,
    status_code=200,
    responses=get_responses(
        [
            ResponseModel(status_code=404, description="Разрешение не найдено"),
        ]
    ),
)
async def update_permission(
    id_: UUID,
    data: UpdatePermissionSchema,
    service: PermissionService = Depends(ServiceFactory.get_permission_service),
):
    return await service.update_permission(id_, data)
