# src/main.py
import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import settings
from app.utils.logging import LOGGING_CONFIG
from app.routes.profiles_routes import router as user_router

logging.config.dictConfig(LOGGING_CONFIG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Service is starting up...")
    yield
    logging.info("Service is shutting down...")


def create_app() -> FastAPI:
    app = FastAPI(
        docs_url=f"/api/{settings.app_name.split('-')[0]}/docs",
        redoc_url=f"/api/{settings.app_name.split('-')[0]}/redoc",
        openapi_url=f"/api/{settings.app_name.split('-')[0]}/openapi.json",
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
    )

    @app.get(f"api/{settings.app_name.split('-')[0]}/health")
    async def health_check():
        return {"status": "ok"}

    # Подключаем роутеры
    app.include_router(user_router)

    return app


app = create_app()
