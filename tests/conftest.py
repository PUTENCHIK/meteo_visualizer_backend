import pytest
from fastapi.testclient import TestClient
from app import app


@pytest.fixture
def test_client():
    """Фикстура создания экземпляра TestClient для каждого теста"""
    with TestClient(app) as client:
        yield client
