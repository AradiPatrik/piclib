from typing import Sequence

from sqlalchemy import delete, select, update, desc
from sqlalchemy.orm import Session, selectinload
from datetime import datetime
import logging


from . import models, schemas

logger = logging.Logger(__name__)


def create_book(db: Session, book_create: schemas.BookCreate) -> models.Book:
    book = models.Book(**book_create.model_dump(), date_added=datetime.now())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_books(db: Session):
    statement = select(models.Book)
    return db.execute(statement).scalars().all()


def delete_book(db: Session, isbn: str):
    statement = delete(models.Book).where(models.Book.isbn == isbn)
    db.execute(statement)
    db.commit()


def create_lend(db: Session, slack_id: str, isbn: str) -> models.Lend:
    lend = models.Lend(slack_id=slack_id, isbn=isbn, lend_date=datetime.now())
    db.add(lend)
    db.commit()
    db.refresh(lend)
    return lend


def get_lends(db: Session):
    statement = select(models.Lend)
    return db.execute(statement).scalars().all()


def get_lends_of_user(db: Session, slack_id: str):
    statement = select(models.Lend).where(models.Lend.slack_id == slack_id)
    return db.execute(statement).scalars().all()


def return_book(db: Session, slack_id: str, isbn: str):
    statement = update(models.Lend) \
        .where(
        models.Lend.slack_id == slack_id,
        models.Lend.isbn == isbn
    ).values(return_date=datetime.now())

    db.execute(statement)
    db.commit()


def get_books_with_lends(db: Session) -> Sequence[models.Book]:
    statement = select(models.Book).options(selectinload(models.Book.lends))
    return db.execute(statement).scalars().all()