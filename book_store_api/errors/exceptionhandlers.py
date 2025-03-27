from typing import Callable

from starlette.requests import Request

from book_store_api.errors.exceptions import BookNotFoundError, BookStoreApiError, ErrorInDBC, MemberNotFound
from fastapi import FastAPI
from fastapi.responses import JSONResponse


def create_exception_handler(
    status_code: int, initial_details: str
) -> Callable[[Request, BookStoreApiError], JSONResponse]:
    detail = {"message": initial_details}

    async def exception_handler(_: Request, exc: BookStoreApiError) -> JSONResponse:
        if exc.message:
            detail["message"] = exc.message

        if exc.name:
            detail["message"] = f"{detail['message']} [{exc.name}]"

        # logger inshallah
        return JSONResponse(
            status_code=status_code, content={"detail": detail["message"]}
        )

    return exception_handler  # type: ignore


def register_exception_handlers(app: FastAPI) -> None:
    """Register app exception handlers."""
    app.add_exception_handler(
        exc_class_or_status_code=BookNotFoundError, handler=create_exception_handler(404, "Ma b3rf")  # type: ignore
    )
    app.add_exception_handler(
        exc_class_or_status_code=MemberNotFound,
        handler=create_exception_handler(409, "ma b3rf"),  # type: ignore
    )
    app.add_exception_handler(
        exc_class_or_status_code=ErrorInDBC,
        handler=create_exception_handler(409, "ma b3rf"),  # type: ignore
    )
