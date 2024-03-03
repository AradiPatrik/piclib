from datetime import datetime, timedelta
import timeit
from sqlalchemy import create_engine, StaticPool, insert
from sqlalchemy.orm import Session

import picc_lib.mappers
from picc_lib.crud import get_books_with_lends
from picc_lib.models import Lend
from picc_lib.models import Book

from picc_lib.tests.seed import book, lend

from picc_lib.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite+pysqlite:///performance.db"


def create_db_engine():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True
    )

    Base.metadata.create_all(bind=engine)

    return engine


def seed_performance_db_data():
    engine = create_db_engine()
    with Session(engine) as session:
        for i in range(40):
            print(i)
            book(session, f"title_{i}", f"author_{i}", f"{i}")
            lends = [
                Lend(
                    slack_id="user",
                    isbn=f"{i}",
                    lend_date=datetime.now() - timedelta(days=j),
                    return_date=datetime.now() - timedelta(days=j)
                ) for j in range(5000)
            ]
            session.bulk_save_objects(lends)
            session.commit()


if __name__ == '__main__':
    db = create_db_engine()
    with Session(db) as session:
        def test_this():
            items = get_books_with_lends(session)
            picc_lib.mappers.to_books_with_availabilities(items)

        selectinload = timeit.timeit(test_this, number=10)
        print(selectinload)
