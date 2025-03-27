from book_store_api.application.book_service import BookService
from book_store_api.domain.entities.book import Book
from book_store_api.errors.exceptions import BookNotFoundError
from book_store_api.presentation.models.book import BookJoined, BookRequest, BookUpdateRequest
from fastapi import APIRouter

book_router = APIRouter()

book_service = BookService()


@book_router.post("/books")
async def create_book(book: BookRequest) -> Book | None:
    book_bean = Book(**book.to_dict())
    result = await book_service.insert(book_bean)
    return result if isinstance(result, Book) else None


@book_router.get("/books/{id}")
async def get_book_by_id(id: int) -> Book | None:
    book_bean = await book_service.fetch(id)
    if isinstance(book_bean, Book):
        return book_bean
    raise BookNotFoundError("Book not found")


@book_router.get("/books", response_model=list[BookJoined])
async def get_all_books(page_size: int = 5) -> list[BookJoined] | None:
    book_bean = await book_service.fetch_all(page_size=page_size)
    if isinstance(book_bean, list) and all(
        isinstance(book, BookJoined) for book in book_bean
    ):
        return book_bean

    return None


@book_router.patch("/books/{book_id}")
async def update_book(book_id: int, book: BookUpdateRequest) -> Book | None:
    result = await book_service.update(book_id, data=book.to_dict())
    if isinstance(result, Book):
        return result
    return None


@book_router.delete("/books/{book_id}")
async def delete_book(book_id: int) -> Book | None:
    result = await book_service.delete(book_id)
    if isinstance(result, Book):
        return result
    return None


@book_router.post("/books/{book_id}/{member_id}")
async def borrow_book(book_id: int, member_id: int) -> Book | None:
    result = await book_service.borrow_book(book_id, member_id)
    if isinstance(result, Book):
        return result
    return None


@book_router.post("/books/{book_id}")
async def return_book(book_id: int) -> Book | None:
    result = await book_service.return_book(book_id)
    if isinstance(result, Book):
        return result
    return None
