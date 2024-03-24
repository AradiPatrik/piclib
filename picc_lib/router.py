import datetime
from typing import Annotated, Tuple, Sequence
from fastapi import Depends, FastAPI
from sqlalchemy import Row
from sqlalchemy.orm import Session

from picc_lib import crud, models, schemas
from picc_lib.database import SessionLocal, engine
import picc_lib.mappers as mappers

import logging

logger = logging.Logger(__name__)

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
    return crud.get_books(db)


@app.get("/books/availability/", response_model=list[schemas.BookWithAvailability])
def return_book_availability(db: DependDb):
    return mappers.to_books_with_availabilities(crud.get_books_with_lends(db=db))


@app.delete("/books/{isbn}/")
def delete_book(isbn: str, db: DependDb):
    crud.delete_book(db, isbn)


@app.post("/lends/{user_id}/")
def create_lend(user_id: str, lend: schemas.LendCreate, db: DependDb):
    crud.create_lend(db, user_id, lend.isbn)


@app.get("/lends/{slack_id}/", response_model=list[schemas.Lend])
def get_lends_of_user(slack_id: str, db: DependDb):
    return crud.get_lends_of_user(db, slack_id)


@app.post("/lends/{slack_id}/{isbn}/return/")
def return_book(slack_id: str, isbn: str, db: DependDb):
    crud.return_book(db, slack_id, isbn)
