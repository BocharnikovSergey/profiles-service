# src/main.py
import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import settings
from app.utils.logging import LOGGING_CONFIG
from app.routes.profiles_routes import router as user_router
from app.middlerware.auth import AuthContextMiddleware

logging.config.dictConfig(LOGGING_CONFIG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Service is starting up...")
    yield
    logging.info("Service is shutting down...")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )

    # Регистрируем middleware
    app.add_middleware(AuthContextMiddleware)

    # Подключаем роутеры
    app.include_router(user_router)

    return app


app = create_app()
