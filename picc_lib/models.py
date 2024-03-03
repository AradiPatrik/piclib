import dataclasses

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base
from datetime import datetime


@dataclasses.dataclass
class Book(Base):
    __tablename__ = "books"

    date_added: Mapped[datetime]
    isbn: Mapped[str] = mapped_column(String(13), primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(100))

    lends: Mapped[list["Lend"]] = relationship(back_populates="book",order_by='desc(Lend.lend_date)', lazy='dynamic')


class Lend(Base):
    __tablename__ = "lends"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    slack_id: Mapped[str] = mapped_column(index=True)
    isbn: Mapped[str] = mapped_column(ForeignKey("books.isbn"), index=True)
    lend_date: Mapped[datetime] = mapped_column(index=True)
    return_date: Mapped[datetime | None]

    book: Mapped["Book"] = relationship(back_populates="lends")

