from typing import Optional

from pydantic import BaseModel


class UserInput(BaseModel):
    name: str
    surname: str
    patronymic: Optional[str]
    phone: int
    text: Optional[str]
