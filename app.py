from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from starlette.exceptions import HTTPException

from src.config import config
from src.db import async_session_maker
from src.managers import TokenManager
from src.routers import (
    auth_router,
    complexes_router,
    mast_configs_router,
    mast_yards_router,
    masts_router,
    permission_router,
    roles_router,
    users_router,
)
from src.utils import create_error_response
from src.utils.exceptions import (
    AppException,
    ExceptionCode,
)
from src.utils.initial_data import InitialDataManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await TokenManager().ping()
    async with async_session_maker() as session:
        manager = InitialDataManager()
        await manager.sync(session)
        await session.commit()

    yield

    await TokenManager().client.close()


app = FastAPI(lifespan=lifespan)
api_prefix = "/api"
app.include_router(auth_router, prefix=api_prefix)
app.include_router(roles_router, prefix=api_prefix)
app.include_router(permission_router, prefix=api_prefix)
app.include_router(users_router, prefix=api_prefix)
app.include_router(complexes_router, prefix=api_prefix)
app.include_router(masts_router, prefix=api_prefix)
app.include_router(mast_configs_router, prefix=api_prefix)
app.include_router(mast_yards_router, prefix=api_prefix)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allow_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Authorization",
        "Access-Control-Allow-Origin",
    ],
)


@app.get("/api/status")
def status():
    """Проверить доступность API"""
    return Response("success")


@app.exception_handler(AppException)
def app_exception_handler(request: Request, ex: AppException):
    return create_error_response(
        status_code=ex.status_code, code=ex.code, message=str(ex)
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return create_error_response(exc.status_code, ExceptionCode.HTTP_ERROR, exc.detail)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    msg = f"Ошибка валидации: {errors[0]['msg']} (поле: {errors[0]['loc'][-1]})"
    return create_error_response(422, ExceptionCode.VALIDATION, msg)
