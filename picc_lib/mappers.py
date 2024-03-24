import datetime
from typing import Sequence, Tuple, Any

from sqlalchemy import Row

from picc_lib import models, schemas


def to_books_with_availabilities(
    rows: Sequence[
        Row[Tuple[models.Book, models.Lend | None, datetime.datetime | None]]
    ]
) -> list[schemas.BookWithAvailability]:
    result = []
    for book, lend, _ in rows:
        is_available = lend is None or lend.return_date is not None
        availability = schemas.BookWithAvailability(
            title=book.title,
            author=book.author,
            isbn=book.isbn,
            availability=schemas.BookAvailability(
                is_available=is_available,
                slack_id=lend.slack_id if not is_available and lend else None,
                expected_return_date=(
                    lend.lend_date + datetime.timedelta(weeks=4)
                    if not is_available and lend
                    else None
                ),
            ),
        )
        result.append(availability)
    return result
