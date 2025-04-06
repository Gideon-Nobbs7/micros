from unittest.mock import MagicMock, patch

import pytest
from ..db import models
from fastapi import HTTPException
from fastapi.testclient import TestClient

# Import the FastAPI app and dependencies
from ..main import app
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..utils import get_db

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Fixture for the database
@pytest.fixture
def test_db():
    # Create the test database and tables
    models.Base.metadata.create_all(bind=engine)

    # Create a dependency override
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    # Use the override for the dependency
    app.dependency_overrides[get_db] = override_get_db

    # Setup: add test data
    db = TestingSessionLocal()
    db.query(models.Fare).delete()

    test_fares = [
        models.Fare(id=1, location="Mountain Trek", price=100, difficulty="Hard"),
        models.Fare(id=2, location="Beach Tour", price=50, difficulty="Easy"),
        models.Fare(id=3, location="Forest Adventure", price=75, difficulty="Medium"),
    ]

    db.add_all(test_fares)
    db.commit()

    yield

    # Teardown: clean up
    db.query(models.Fare).delete()
    db.commit()
    db.close()
    models.Base.metadata.drop_all(bind=engine)


# Fixture for the test client
@pytest.fixture
def client(test_db):
    with TestClient(app) as c:
        yield c


# Test the root endpoint
def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert response.json() == "Server is running", f"Expected 'Server is running', got {response.json()}"


# Test getting all fares
def test_get_all_fares(client):
    response = client.get("/api/products")
    assert response.status_code == 200
    fares = response.json()

    assert len(fares) == 3
    assert fares[0]["location"] == "Mountain Trek"
    assert fares[1]["price"] == 50
    assert fares[2]["difficulty"] == "Medium"


# Test the like endpoint with mocked request
@patch("requests.get")
def test_like_product(mock_get, client):
    # Mock the response from the user API
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": 1, "username": "testuser"}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    response = client.post("/api/products/1/like")
    assert response.status_code == 200

    # Verify our mock was called with the correct URL
    mock_get.assert_called_once_with("http://localhost/api/user")


# Test that exceptions are properly handled
def test_get_fares_exception(client):
    # Override the get_db dependency to raise an exception
    def override_get_db_exception():
        raise HTTPException(status_code=500, detail="Database Error")

    # Save the original override to restore it after the test
    original_override = app.dependency_overrides[get_db]
    app.dependency_overrides[get_db] = override_get_db_exception

    # The endpoint should return a 500 error
    response = client.get("/api/products")
    assert response.status_code == 500

    # Restore the original override
    app.dependency_overrides[get_db] = original_override


if __name__ == "__main__":
    pytest.main()
