from typing import Sequence, Tuple, Any

from sqlalchemy import Row

from picc_lib import models, schemas


def to_book_with_availability(book: models.Book) -> schemas.BookWithAvailability:
    last_lend: models.Lend | None = next(iter(book.lends.limit(1).all()), None)
    has_lend_record = last_lend is not None
    is_returned = has_lend_record and last_lend.return_date is not None
    is_available = not has_lend_record or is_returned
    return schemas.BookWithAvailability(
        title=book.title,
        author=book.author,
        isbn=book.isbn,
        availability=schemas.BookAvailability(
            is_available=is_available,
            slack_id=None if is_available else last_lend.slack_id,
            return_date=None if is_available else last_lend.return_date,
        )
    )

def to_books_with_availabilities(rows: Sequence[Row[Tuple[Any, ...]]]):
    return [schemas.BookWithAvailability(
        title=book.title,
        author=book.author,
        isbn=book.isbn,
        availability=schemas.BookAvailability(
            is_available=lend.lend_date is None or lend.return_date is not None,
            slack_id=lend.slack_id,
            return_date=lend.return_date,
        )
    ) for book, lend, _ in rows]