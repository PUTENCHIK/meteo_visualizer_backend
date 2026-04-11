from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

from src.routers import auth_router, roles_router
from src.utils.exceptions import (
    AppException,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
api_prefix = "/api"
app.include_router(auth_router, prefix=api_prefix)
app.include_router(roles_router, prefix=api_prefix)


@app.get("/api/status")
def status():
    """Проверить доступность API"""
    return Response("success")


@app.exception_handler(AppException)
def handle_exception(request: Request, ex: AppException):
    return JSONResponse(status_code=ex.status_code, content={"details": str(ex)})
