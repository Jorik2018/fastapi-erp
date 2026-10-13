# fastapi_erp/middleware/security.py

import os
import traceback

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from fastapi_erp.security import decode_token


class JWTMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        path = request.url.path

        if path in (
            "/docs",
            "/openapi.json",
            "/redoc",
        ):
            return await call_next(request)

        if (
            os.getenv("MOCK_VAULT", "false").lower() == "true"
        ):
            return await call_next(request)

        authorization = request.headers.get("Authorization")

        if not authorization:
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header required"}
            )

        scheme, _, token = authorization.partition(" ")

        if scheme.lower() != "bearer" or not token:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid authorization header"}
            )
        try:
            claims = decode_token(token)

        except Exception as exc:
            print("JWT MIDDLEWARE ERROR")
            print("TYPE:", type(exc).__name__)
            print("MESSAGE:", str(exc))
            traceback.print_exc()

            status_code = getattr(exc, "status_code", 401)
            detail = getattr(exc, "detail", str(exc) or "Invalid token")

            return JSONResponse(
                status_code=status_code,
                content={"detail": detail}
            )

        # Guardamos los claims para el resto del request
        request.state.user = claims

        return await call_next(request)