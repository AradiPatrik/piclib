import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session, sessionmaker
from ..database import Base
from ...router import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite+pysqlite:///:memory:"


@pytest.fixture(scope='function')
def db_engine():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)
    yield engine

    engine.dispose()


@pytest.fixture(scope='function')
def db_session_factory(db_engine):
    return sessionmaker(bind=db_engine)


@pytest.fixture(scope='function')
def db_session(db_session_factory):
    session: Session = db_session_factory()

    def override_get_db():
        db = session
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield session

    session.close()
