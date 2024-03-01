from collections.abc import Sequence
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

from picc_lib.models import Lend

from .. import crud
from . import seed
from .. import models

from picc_lib.main import app

client = TestClient(app)


def is_recent(date_time, seconds=10):
    return datetime.now() - timedelta(seconds=seconds) <= date_time <= datetime.now()

def test_add_book(db_session):
    # WHEN
    response = client.post(
        "/books/", json={"isbn": "123456789098", "title": "Eat", "author": "John Mary"}
    )

    # THEN
    assert response.status_code == 200
    data = response.json()
    assert data["isbn"] == "123456789098"
    assert data["title"] == "Eat"
    assert data["author"] == "John Mary"
    resp_datetime = datetime.fromisoformat(data["date_added"])
    assert datetime.now() - timedelta(seconds=10) <= resp_datetime <= datetime.now()

    books = crud.get_books(db_session)
    assert len(books) == 1
    assert books[0].isbn == "123456789098"
    assert books[0].author == "John Mary"
    assert books[0].title == "Eat"
    assert is_recent(books[0].date_added)


def test_get_books(db_session):
    # GIVEN
    seed_book = seed.book(db_session, author="Ting")

    # WHEN
    response = client.get(
        "/books/",
    )

    # THEN
    assert response.status_code == 200
    data = response.json()
    assert data[0]["isbn"] == seed_book.isbn
    assert data[0]["title"] == seed_book.title
    assert data[0]["author"] == seed_book.author


def test_delete_book(db_session):
    # GIVEN
    seed.book(db_session, isbn="123")

    # WHEN
    response = client.delete("/books/123/")

    # THEN
    assert response.status_code == 200

    books = crud.get_books(db_session)
    assert len(books) == 0


def test_lend_book_to_new_user(db_session):
    # GIVEN
    seed.book(db_session, isbn="123")

    # WHEN
    response = client.post(
        "/lends/yanbin",
        json={"isbn": "123"}
    )

    # THEN
    assert response.status_code == 200

    lends: Sequence[Lend] = crud.get_lends(db_session)
    assert len(lends) == 1
    assert lends[0].isbn == "123"
    assert lends[0].slack_id == "yanbin"
    assert is_recent(lends[0].lend_date)
    assert lends[0].return_date is None


def test_GIVEN_user_has_books_WHEN_get_books_THEN_return_book_list(db_session):
    # GIVEN
    seed.book(db_session, isbn="123")
    seed.lend(db_session, slack_id="yanbin", isbn="123")

    # WHEN
    response = client.get("/lends/yanbin")

    # THEN
    assert response.status_code == 200

    lends = response.json()
    assert len(lends) == 1
    assert lends[0]["isbn"] == "123"
    assert lends[0]["slack_id"] == "yanbin"
    lend_date = datetime.fromisoformat(lends[0]["lend_date"])
    assert is_recent(lend_date)
    assert lends[0]["return_date"] is None

def test_GIVEN_user_has_no_books_WHEN_get_books_THEN_return_empty_list(db_session):
    # WHEN
    response = client.get("/lends/yanbin")

    # THEN
    assert response.status_code == 200

    lends = response.json()
    assert len(lends) == 0


def test_GIVEN_user_has_lend_WHEN_update_lend_date_THEN_lend_date_should_update(db_session):
    # GIVEN
    seed.book(db_session, isbn="123")
    seed.lend(db_session, slack_id="yanbin", isbn="123")

    # WHEN
    response = client.post("/lends/yanbin/123/return")

    assert response.status_code == 200

    # THEN
    lends: Sequence[models.Lend] = crud.get_lends_of_user(
        db_session, slack_id="yanbin")

    assert lends[0].return_date is not None
    assert is_recent(lends[0].return_date, seconds=1)

