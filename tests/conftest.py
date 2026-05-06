import pytest
from fastapi.testclient import TestClient

from app.database import db
from app.main import app


@pytest.fixture(autouse=True)
def reset_database():
    db.reset()


@pytest.fixture
def client():
    return TestClient(app)
