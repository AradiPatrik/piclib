import os
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import (
    create_engine,
)

DB_URL = os.getenv("DB_URL")
if DB_URL is None:
    raise RuntimeError("DB_URL is not in environment")

engine = create_engine(
    DB_URL,
    echo=True,
)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
