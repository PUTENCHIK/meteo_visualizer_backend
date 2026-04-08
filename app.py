from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import Response


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/api/status")
def status():
    """Проверить доступность API"""
    return Response("success")
