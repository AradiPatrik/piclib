from pydantic import BaseModel, ConfigDict
from datetime import datetime


class BaseBook(BaseModel):
    title: str
    author: str
    isbn: str


class Book(BaseBook):
    model_config = ConfigDict(from_attributes=True)
    date_added: datetime


class BookCreate(BaseBook):
    pass


class BookAvailability(BaseModel):
    is_available: bool
    slack_id: str | None
    expected_return_date: datetime | None


class BookWithAvailability(BaseBook):
    availability: BookAvailability


class LendCreate(BaseModel):
    isbn: str


class Lend(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    isbn: str
    slack_id: str
    lend_date: datetime
    return_date: datetime | None
