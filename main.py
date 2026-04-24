import sys
import asyncio
import uvicorn

from src.config import config


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == "__main__":
    uvicorn.run(
        app="app:app",
        host=config.app_host,
        port=config.app_port,
        reload=config.app_reload,
    )
