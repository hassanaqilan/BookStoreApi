from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection

from book_store_api.domain.entities.book import Book
from book_store_api.infrastructure.db.connection import book_table, member_table
from book_store_api.infrastructure.repo.base_repo import BaseRepo
from book_store_api.presentation.models.book import BookJoined


class BookRepo(BaseRepo[Book]):
    def __init__(self) -> None:
        super().__init__(table=book_table, entity=Book)

    async def fetch_all(
        self,
        page_size: int = 5,
        offset: int = 0,
        connection: Optional[AsyncConnection] = None,
    ) -> list[BookJoined] | None:

        stmt = (
            select(self.table, member_table.c.email, member_table.c.name)
            .limit(page_size)
            .offset(offset)
            .join(
                member_table,
                self.table.c.borrowed_by == member_table.c.id,
                isouter=True,
            )
        )

        if not connection:
            return None

        res = await connection.execute(stmt)
        result = res.fetchall()

        if result is None:
            return None

        return [BookJoined(**res._mapping) for res in result]
