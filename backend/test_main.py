import pytest
from fastapi.testclient import TestClient
from main import app


# Create the test client for interacting with FastAPI
@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

def test_read_root(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_retrieve_document(client):
    """Test /retrieve-document endpoint."""
    response = client.get("/retrieve-document")
    assert response.status_code == 200
    data = response.json()
    assert "document" in data
    assert data["document"] is not None  # Ensure document is returned, could be a placeholder if empty.