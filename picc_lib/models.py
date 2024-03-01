from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base
from datetime import datetime


class Book(Base):
    __tablename__ = "books"

    isbn: Mapped[str] = mapped_column(String(13),primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(100))
    date_added: Mapped[datetime]

class Lend(Base):
    __tablename__ = "lends"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    slack_id: Mapped[str] = mapped_column(index=True)
    isbn: Mapped[str] = mapped_column(ForeignKey("books.isbn"))
    lend_date: Mapped[datetime]
    return_date: Mapped[datetime | None]

