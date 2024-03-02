from typing import Annotated
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from picc_lib import crud, models, schemas
from picc_lib.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DependDb = Annotated[Session, Depends(get_db)]


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: DependDb):
    return crud.create_book(db, book)


@app.get("/books/", response_model=list[schemas.Book])
def get_books(db: DependDb):
    books = crud.get_books(db)
    return books


@app.get("/books/availability/", response_model=list[schemas.BookWithAvailability])
def return_book_availability(db: DependDb):
    books_with_lends = crud.get_books_with_lends(db)
    result = []
    for book in books_with_lends:
        sorted_lends = sorted(book.lends, key=lambda l: l.lend_date, reverse=True)
        last_lend: models.Lend | None = sorted_lends[0] if sorted_lends else None
        has_lend_record = last_lend is not None
        is_returned = has_lend_record and last_lend.return_date is not None
        is_available = not has_lend_record or is_returned

        result.append(
            schemas.BookWithAvailability(
                title=book.title,
                author=book.author,
                isbn=book.isbn,
                availability=schemas.BookAvailability(
                    is_available=is_available,
                    slack_id=None if is_available else last_lend.slack_id,
                    return_date=None if is_available else last_lend.return_date,
                )
            )
        )
    return result


@app.delete("/books/{isbn}/")
def delete_book(isbn: str, db: DependDb):
    crud.delete_book(db, isbn)


@app.post("/lends/{user_id}/")
def create_lend(user_id: str, lend: schemas.LendCreate, db: DependDb):
    crud.create_lend(db, user_id, lend.isbn)


@app.get("/lends/{slack_id}/", response_model=list[schemas.Lend])
def get_lends_of_user(slack_id: str, db: DependDb):
    lends = crud.get_lends_of_user(db, slack_id)
    return lends


@app.post("/lends/{slack_id}/{isbn}/return/")
def return_book(slack_id: str, isbn: str, db: DependDb):
    crud.return_book(db, slack_id, isbn)
