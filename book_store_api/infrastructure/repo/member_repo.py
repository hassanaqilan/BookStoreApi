from book_store_api.domain.entities.member import Member
from book_store_api.infrastructure.db.connection import member_table
from book_store_api.infrastructure.repo.base_repo import BaseRepo


class MemberRepo(BaseRepo[Member]):
    def __init__(self) -> None:
        super().__init__(table=member_table, entity=Member)
