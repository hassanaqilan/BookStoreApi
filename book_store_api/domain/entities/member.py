from dataclasses import dataclass
from datetime import datetime
from typing import Any

from book_store_api.domain.entities.base_entity import BaseEntity


@dataclass
class Member(BaseEntity):
    name: str
    email: str

    def __init__(
        self,
        name: str,
        email: str,
        id: int = 0,
        created_at: datetime = datetime.today(),
    ) -> None:
        self.name = name
        self.email = email
        self.id = id
        self.created_at = created_at
        super().__init__(id, created_at)

    def to_dict(self) -> dict[str, Any]:
        mydict = {
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at if self.created_at else datetime.today(),
        }
        return mydict
