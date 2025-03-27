from contextlib import asynccontextmanager
from functools import wraps
from typing import Any, AsyncIterator, Awaitable, Callable

from sqlalchemy.ext.asyncio import AsyncConnection

from book_store_api.infrastructure.db.connection import engine


@asynccontextmanager
async def unit_of_work() -> AsyncIterator[AsyncConnection]:
    """Async context manager for handling the unit of work pattern."""
    connection: AsyncConnection = await engine.connect()
    transaction = await connection.begin()

    try:
        yield connection
        await transaction.commit()
    except Exception as e:
        await transaction.rollback()
        raise e
    finally:
        await connection.close()


def uow(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    """Decorator to manage Unit of Work"""

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        async with unit_of_work() as connection:  # type: AsyncConnection
            return await func(*args, connection=connection, **kwargs)  # Ensure await

    return wrapper  # Return the async function properly
