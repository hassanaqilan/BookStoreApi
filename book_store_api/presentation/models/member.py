from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field, constr


class MemberUpdate(BaseModel):
    name: constr(min_length=1, strip_whitespace=True) | None = None  # type: ignore
    email: EmailStr | None = None

    def to_dict(self) -> dict[str, Any]:
        mydict = {}
        if self.email:
            mydict["email"] = self.email
        if self.name:
            mydict["name"] = self.name
        return mydict


class MemberCreate(BaseModel):
    name: constr(min_length=1, strip_whitespace=True) = Field(  # type: ignore
        examples=["Arab got talent"], description="name ya bro "
    )
    email: EmailStr = Field(
        examples=["hassan@gmail.com", "Khlaed@gmail.com"], description="Email ya bro "
    )

    def to_dict(self) -> dict[str, Any]:
        mydict = {
            "name": self.name,
            "email": self.email,
            "created_at": datetime.today(),
        }
        return mydict
