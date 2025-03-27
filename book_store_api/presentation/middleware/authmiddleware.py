from typing import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from book_store_api.config import Config
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

DUMMY_API_KEY = Config.DUMMY_API_KEY
app = FastAPI()

# OAuth2 scheme for Swagger UI authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:

        # Allow open access to login and Swagger routes
        if request.url.path in ("/login", "/docs", "/openapi.json"):
            return await call_next(request)

        # Check for API token in request headers (Bearer Token)
        authorization = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            return JSONResponse({"error": "Missing or invalid token"}, status_code=401)

        token = authorization.split("Bearer ")[-1]
        if token != DUMMY_API_KEY:
            return JSONResponse({"error": "Unauthorized"}, status_code=401)

        return await call_next(request)
