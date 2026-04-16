from typing import Optional

from fastapi import APIRouter, Cookie, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from src.factories import ServiceFactory
from src.schemas import (
    AuthTokensSchema,
    ResponseModel,
    SigninSchema,
    SignupSchema,
)
from src.services import AuthService
from src.utils import get_responses

auth_router = APIRouter(prefix="/auth", tags=["Авторизация"])


@auth_router.post(
    "/signin",
    response_model=AuthTokensSchema,
    status_code=200,
    responses=get_responses(
        [
            ResponseModel(status_code=401, description="Неверный пароль"),
            ResponseModel(status_code=404, description="Пользователь не найден"),
        ],
        include_auth=False,
    ),
)
async def signin(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(ServiceFactory.get_auth_service),
):
    data = SigninSchema(login=form_data.username, password=form_data.password)
    return await service.signin(data, response)


@auth_router.post(
    "/signup",
    response_model=AuthTokensSchema,
    status_code=200,
    responses=get_responses(
        [
            ResponseModel(status_code=409, description="Логин уже используется"),
        ],
        include_auth=False,
    ),
)
async def signup(
    response: Response,
    data: SignupSchema,
    service: AuthService = Depends(ServiceFactory.get_auth_service),
):
    return await service.signup(data, response)


@auth_router.post(
    "/refresh",
    response_model=AuthTokensSchema,
    status_code=200,
    responses=get_responses(
        [
            ResponseModel(status_code=401, description="Токен устарел"),
            ResponseModel(status_code=401, description="Невалидный токен"),
        ],
        include_auth=False,
    ),
)
async def refresh_tokens(
    response: Response,
    refresh_token: Optional[str] = Cookie(None),
    service: AuthService = Depends(ServiceFactory.get_auth_service),
):
    return await service.refresh(refresh_token, response)


@auth_router.post(
    "/logout",
    status_code=204,
    responses=get_responses(
        include_auth=False,
    ),
)
async def logout(
    response: Response,
    refresh_token: Optional[str] = Cookie(None),
    service: AuthService = Depends(ServiceFactory.get_auth_service),
):
    await service.logout(refresh_token, response)
