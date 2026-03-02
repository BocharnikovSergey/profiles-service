from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from starlette.responses import JSONResponse


class AuthContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        user_data = getattr(request.state, "user_data", None)

        if not user_data:
            return JSONResponse(
                status_code=401,
                content={"detail": "Unauthorized"},
            )

        # ---- нормализация ----
        try:
            request.state.user_id = int(user_data["sub"])
            request.state.is_active = user_data.get("is_active", False)
            request.state.is_superuser = user_data.get("is_superuser", False)
        except (KeyError, ValueError):
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid user data"},
            )

        # ---- проверка активности ----
        if not request.state.is_active:
            return JSONResponse(
                status_code=403,
                content={"detail": "User is not active"},
            )

        response = await call_next(request)
        return response
