from fastapi import APIRouter, Depends

from src.factories import ServiceFactory
from src.schemas import (
    AuthTokensSchema,
    ResponseModel,
    SigninSchema,
    SignupSchema,
    UserSchema,
)
from src.services import AuthService
from src.utils import default_responses

auth_router = APIRouter(prefix="/auth", tags=["Авторизация"])


@auth_router.post(
    "/signin",
    response_model=AuthTokensSchema,
    status_code=200,
    responses=default_responses(
        [
            ResponseModel(status_code=401, description="Неверный пароль"),
            ResponseModel(status_code=404, description="Пользователь не найден"),
        ]
    ),
)
async def signin(
    data: SigninSchema, service: AuthService = Depends(ServiceFactory.get_auth_service)
):
    return await service.signin(data)


@auth_router.post(
    "/signup",
    response_model=UserSchema,
    status_code=200,
    responses=default_responses(
        [
            ResponseModel(status_code=409, description="Логин уже используется"),
        ]
    ),
)
async def signup(
    data: SignupSchema, service: AuthService = Depends(ServiceFactory.get_auth_service)
):
    return await service.signup(data)
