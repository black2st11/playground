from pytest import fixture
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session

from app.core.config import settings
from app.db.base_class import Base


@fixture(scope="session")
def db():
    engine = create_engine(settings.SQLALCHEMY_TEST_DATABASE_URL)
    return {"connection": engine.connect(), "engine": engine}


@fixture(scope="function")
def setup_database(db):
    Base.metadata.create_all(db["connection"])
    yield
    Base.metadata.drop_all(db["connection"])


@fixture
def db_session(setup_database, db):
    yield scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=db["connection"])
    )
