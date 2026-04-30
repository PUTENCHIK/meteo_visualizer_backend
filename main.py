import uvicorn

from src.config import config

if __name__ == "__main__":
    uvicorn.run(
        app="app:app",
        host=config.app_host,
        port=config.app_port,
        reload=config.app_reload,
    )
