from typing import Any, Generic, Optional, Type, TypeVar

from sqlalchemy import Table, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncConnection

from book_store_api.domain.entities.base_entity import BaseEntity

E = TypeVar("E", bound="BaseEntity")


class BaseRepo(Generic[E]):

    def __init__(self, table: Table, entity: Type[E]) -> None:
        self.entity = entity
        self.table = table

    async def insert(
        self, entity: E, connection: Optional[AsyncConnection] = None
    ) -> E | None:

        if not connection:
            raise ConnectionRefusedError("Check the docker container")

        stmt = (
            insert(self.table).returning(*self.table.columns).values(**entity.to_dict())
        )
        res = await connection.execute(stmt)

        result = res.fetchone()
        if result is None:
            return None
        return self.entity(**result._mapping)

    async def fetch(
        self, entity_id: int, connection: Optional[AsyncConnection] = None
    ) -> E | None:
        stmt = select(self.table).where(self.table.c.id == entity_id)

        if not connection:
            return None

        res = await connection.execute(stmt)
        result = res.fetchone()

        if result is None:
            return None

        return self.entity(**result._mapping)

    async def update(
        self,
        id: int,
        entity: dict[str, Any],
        connection: Optional[AsyncConnection] = None,
    ) -> E | None:
        stmt = (
            update(self.table)
            .returning(*self.table.columns)
            .where(self.table.c.id == id)
            .values(entity)
        )

        if not connection:
            return None

        res = await connection.execute(stmt)
        result = res.fetchone()
        if result is None:
            return None

        return self.entity(**result._mapping)

    async def delete(
        self, id: int, connection: Optional[AsyncConnection] = None
    ) -> E | None:
        stmt = (
            delete(self.table)
            .returning(*self.table.columns)
            .where(self.table.c.id == id)
        )
        if not connection:
            return None

        res = await connection.execute(stmt)
        result = res.fetchone()
        if result is None:
            return None

        return self.entity(**result._mapping)

    async def fetch_all(
        self,
        page_size: int = 5,
        offset: int = 0,
        connection: Optional[AsyncConnection] = None,
    ) -> Any | None:

        if not connection:
            return None

        stmt = select(self.table).limit(page_size).offset(offset)
        res = await connection.execute(stmt)
        result = res.fetchall()
        if result is None:
            return None

        return [self.entity(**res._mapping) for res in result]
