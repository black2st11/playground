import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import URL

from app.core.config import settings

Base = declarative_base()
engine = create_engine(settings.SQLALCHEMY_TEST_DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)


@pytest.fixture(scope="module")
def test_db_session():
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    session.rollback()
    session.close()
