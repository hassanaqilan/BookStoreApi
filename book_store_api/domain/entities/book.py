from dataclasses import dataclass
from datetime import datetime
from typing import Any

from book_store_api.domain.entities.base_entity import BaseEntity
from book_store_api.errors.exceptions import BookAlreadyBorrowed


@dataclass
class Book(BaseEntity):
    title: str
    author: str
    is_borrowed: bool  # true
    borrowed_date: datetime | None  # not none
    borrowed_by: int | None  # not none

    def __init__(
        self,
        title: str,
        author: str,
        is_borrowed: bool = False,
        borrowed_date: datetime | None = None,
        borrowed_by: int | None = None,
        id: int | None = None,
        created_at: datetime | None = None,
    ):
        self.title = title
        self.author = author
        self.is_borrowed = is_borrowed
        self.borrowed_date = borrowed_date
        self.borrowed_by = borrowed_by
        self.id = id
        self.created_at = created_at
        super().__init__(id, created_at)

    def to_dict(self) -> dict[str, Any]:
        mydict = {
            "title": self.title,
            "author": self.author,
            "is_borrowed": self.is_borrowed,
            "borrowed_date": self.borrowed_date,
            "borrowed_by": self.borrowed_by,
            "created_at": self.created_at or datetime.today(),
        }
        return mydict

    def borrow(self, member_id: int) -> "Book":

        if self.is_borrowed:
            raise BookAlreadyBorrowed("is_borrowed is till true man")

        self.borrowed_by = member_id
        self.is_borrowed = True
        self.borrowed_date = datetime.today()
        return self

    def return_book(self) -> "Book":
        self.borrowed_by = None
        self.is_borrowed = False
        self.borrowed_date = None
        return self
