from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncConnection

from book_store_api.domain.entities.member import Member
from book_store_api.infrastructure.repo.member_repo import MemberRepo
from book_store_api.infrastructure.unit_of_work import uow


class MemberService:
    def __init__(self) -> None:
        self.member_repo = MemberRepo()
        pass

    @uow
    async def insert(
        self, member: Member, connection: Optional[AsyncConnection] = None
    ) -> "Member" | Any:
        insert = await self.member_repo.insert(member, connection)
        return insert

    @uow
    async def fetch(self, id: int, connection: Optional[AsyncConnection] = None) -> "Member" | Any:
        fetch = await self.member_repo.fetch(id, connection)
        return fetch

    @uow
    async def fetch_all(self, connection: Optional[AsyncConnection] = None) -> list[Member] | Any:
        fetch_all = await self.member_repo.fetch_all(connection=connection)
        return fetch_all

    @uow
    async def update(
        self, id: int, member: dict[str, Any], connection: Optional[AsyncConnection] = None
    ) -> "Member" | Any:

        old_book = await self.member_repo.fetch(id, connection=connection)
        if not old_book:
            raise NotImplementedError("sorry don't worry exception")

        for key, value in member.items():
            if hasattr(old_book, key):
                setattr(old_book, key, value)
        update = await self.member_repo.update(id, member, connection)
        return update

    @uow
    async def delete(
        self, id: int, connection: Optional[AsyncConnection] = None
    ) -> "Member" | Any:
        delete = await self.member_repo.delete(id, connection=connection)
        return delete
