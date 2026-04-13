from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

from src.db import async_session_maker
from src.managers import TokenManager
from src.routers import auth_router, permission_router, roles_router, users_router
from src.utils.exceptions import (
    AppException,
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


@app.get("/api/status")
def status():
    """Проверить доступность API"""
    return Response("success")


@app.exception_handler(AppException)
def handle_exception(request: Request, ex: AppException):
    return JSONResponse(
        status_code=ex.status_code,
        content={"error": ex.__class__.__name__, "error_description": str(ex)},
        headers={"WWW-Authenticate": "Bearer"},
    )
