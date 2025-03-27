import time
from typing import Any

from book_store_api.config import Config
from book_store_api.errors.exceptionhandlers import register_exception_handlers
from book_store_api.presentation.middleware.authmiddleware import AuthMiddleware
from book_store_api.presentation.routes.book_routes import book_router
from book_store_api.presentation.routes.member_routes import member_router
from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

DUMMY_API_KEY = Config.DUMMY_API_KEY


@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Any) -> Any:
    """
    A middleware to calculate thhe response time
    and put it in header
    """
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Define OAuth2 scheme for Swagger UI (Bearer Token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Customizing Swagger UI to require Bearer Token
def custom_openapi() -> Any:
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Book Store API",
        version="1.0.0",
        description="API requires Bearer Token authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return openapi_schema


app.include_router(book_router, tags=["books"])
app.include_router(member_router, tags=["member"])
app.add_middleware(AuthMiddleware)

register_exception_handlers(app)

app.openapi = custom_openapi  # type: ignore
