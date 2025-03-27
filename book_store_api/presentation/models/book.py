from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, constr

from book_store_api.domain.entities.book import Book


@dataclass
class BookJoined(Book):
    """
    Add the member name and member email attributes to the entity
    used in fetch all books and joined with members
    """

    email: str
    name: str


class BookRequest(BaseModel):
    """
    Book create request

    Attributes:
        name: name of the book that has name
        author: the author name the wrote the book

    """

    title: constr(strip_whitespace=True)  # type: ignore
    author: constr(strip_whitespace=True, min_length=3)  # type: ignore

    def to_dict(self) -> dict[str, Any]:
        return {
            key: value
            for key, value in self.model_dump(exclude_unset=True).items()
            if value is not None
        }


class BookUpdateRequest(BaseModel):
    """
    Book create request

    Attributes:
        name: name of the book that has name
        author: the author name that wrote the book
    """

    name: constr(strip_whitespace=True, min_length=3) | None = None  # type: ignore
    author: constr(strip_whitespace=True, min_length=3) | None = None  # type: ignore

    def to_dict(self) -> dict[str, Any]:
        return {
            key: value
            for key, value in self.model_dump(exclude_unset=True).items()
            if value is not None
        }
