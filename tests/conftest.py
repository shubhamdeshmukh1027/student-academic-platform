import pytest
from app import create_app
from database.db import db


@pytest.fixture(autouse=True)
def clean_db():
    db.reset()
    yield
    db.reset()


@pytest.fixture
def client():
    return create_app().test_client()
