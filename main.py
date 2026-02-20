# src/main.py
from contextlib import asynccontextmanager
import logging.config
from app.routes.profiles_routes import router as user_router
from config import settings
from app.utils.logging import LOGGING_CONFIG
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse

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

    return app


app = create_app()


async def get_current_user_id(x_user_id: str | None) -> str:
    if x_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-User-Id header is missing. Direct access not allowed.",
        )
    return x_user_id


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    x_user_id = request.headers.get("x-user-id")
    try:
        user_id = await get_current_user_id(x_user_id)
        request.state.user_id = user_id
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    response = await call_next(request)
    return response


app.include_router(user_router)
