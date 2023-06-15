import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import URL

from app.core.config import settings

Base = declarative_base()

url = URL.create(
    drivername=settings.TEST_DB_DRIVER,
    username=settings.TEST_DB_USER,
    host=settings.TEST_DB_HOST,
    password=settings.TEST_DB_PASSWORD,
    database=settings.TEST_DB_DATABASE,
)

engine = create_engine("sqlite:///db\\test.db", echo=True)
Session = sessionmaker(bind=engine)


@pytest.fixture(scope="module")
def test_db_session():
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    session.rollback()
    session.close()
