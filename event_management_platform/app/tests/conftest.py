import os
import mongomock
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ['DATABASE_URL'] = 'sqlite:///./test_event_management.db'
os.environ['MONGO_URL'] = 'mongodb://localhost:27017'
os.environ['MONGO_DB_NAME'] = 'test_event_platform'

from app.database import Base, get_db
from app.main import app
from app import mongo

SQLALCHEMY_DATABASE_URL = 'sqlite:///./test_event_management.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def override_mongo(monkeypatch):
    mock_client = mongomock.MongoClient()
    mock_db = mock_client['test_event_platform']
    monkeypatch.setattr(mongo, 'get_mongo_db', lambda: mock_db)
    yield


@pytest.fixture()
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
