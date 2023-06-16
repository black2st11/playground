from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.core.config import settings
from app.db.base_class import Base


@fixture(scope="session")
def connection():
    engine = create_engine(settings.SQLALCHEMY_TEST_DATABASE_URL)
    return engine.connect()


@fixture(scope="session")
def setup_database(connection):
    Base.metadata.bind = connection
    Base.metadata.create_all()
    yield
    Base.metadata.drop_all()


@fixture
def db_session(setup_database, connection):
    transaction = connection.begin()
    yield scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )
