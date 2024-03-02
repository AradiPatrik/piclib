from picc_lib import crud, models
from picc_lib.schemas import BookCreate
from sqlalchemy.orm import Session
from datetime import datetime


def book(
        db: Session,
        title: str = "test_title",
        author: str = "test_author",
        isbn: str = "test_isbn",
):
    return crud.create_book(db, BookCreate(title=title, author=author, isbn=isbn))


def lend(
        db: Session,
        slack_id: str,
        isbn: str,
        lend_date: datetime = datetime.now(),
        return_date: datetime | None = None
):
    lend = models.Lend(slack_id=slack_id, isbn=isbn,
                       lend_date=lend_date, return_date=return_date)
    db.add(lend)
    db.commit()
    db.refresh(lend)
    return lend
