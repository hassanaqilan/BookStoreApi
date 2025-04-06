from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncConnection

from book_store_api.application.base_service import BaseService
from book_store_api.domain.entities.book import Book
from book_store_api.errors.exceptions import BookNotFoundError, ErrorInDBC, MemberNotFound
from book_store_api.infrastructure.repo.book_repo import BookRepo
from book_store_api.infrastructure.repo.member_repo import MemberRepo
from book_store_api.infrastructure.unit_of_work import uow
from book_store_api.presentation.models.book import BookJoined


class BookService(BaseService):

    def __init__(self) -> None:
        self.book_repo = BookRepo()
        self.member_repo = MemberRepo()
        super().__init__()

    @uow
    async def insert(
        self, book: Book, connection: Optional[AsyncConnection] = None
    ) -> Book | None:
        try:
            insert = await self.book_repo.insert(book, connection=connection)
        except ConnectionRefusedError as e:
            raise ErrorInDBC(e.__str__())
        return insert

    @uow
    async def fetch(
        self, id: int, connection: Optional[AsyncConnection] = None
    ) -> Book | None:
        fetch = await self.book_repo.fetch(id, connection=connection)
        return fetch

    @uow
    async def fetch_all(
        self, connection: Optional[AsyncConnection] = None, page_size: int = 5
    ) -> list[BookJoined] | None:
        fetch_all = await self.book_repo.fetch_all(
            connection=connection, page_size=page_size
        )
        return fetch_all

    @uow
    async def update(
        self,
        id: int,
        data: dict[str, Any],
        connection: Optional[AsyncConnection] = None,
    ) -> Book | None:
        # validate it's a book
        old_book = await self.book_repo.fetch(id, connection=connection)
        if not old_book:
            raise BookNotFoundError("sorry don't worry exception")

        for key, value in data.items():
            if hasattr(old_book, key):
                setattr(old_book, key, value)
        update = await self.book_repo.update(
            id, old_book.to_dict(), connection=connection
        )
        return update

    @uow
    async def delete(
        self, id: int, connection: Optional[AsyncConnection] = None
    ) -> Book | None:
        delete = await self.book_repo.delete(id, connection=connection)
        return delete

    @uow
    async def borrow_book(
        self, book_id: int, member_id: int, connection: Optional[AsyncConnection] = None
    ) -> Book | None:

        book_bean = await self.book_repo.fetch(book_id, connection=connection)
        member_bean = await self.member_repo.fetch(member_id, connection=connection)

        if book_bean is None:
            raise BookNotFoundError("No poco phone")
        if member_bean is None:
            raise MemberNotFound("La miembro esta muerta")

        updated_book = book_bean.borrow(member_id)
        result = await self.book_repo.update(
            book_id, updated_book.to_dict(), connection=connection
        )
        return result

    @uow
    async def return_book(
        self, book_id: int, connection: Optional[AsyncConnection] = None
    ) -> Book | None:
        book_bean = await self.book_repo.fetch(book_id, connection=connection)

        if book_bean is None:
            raise BookNotFoundError("No poco phone")

        returned_book = book_bean.return_book()
        result = await self.book_repo.update(
            book_id, returned_book.to_dict(), connection=connection
        )
        return result
