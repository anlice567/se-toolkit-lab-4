"""End-to-end tests for the GET /interactions endpoint."""

import os
import httpx
import pytest


BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
API_TOKEN = os.getenv("API_TOKEN", "my-secret-api-key")


@pytest.fixture
def client():
    """Create an HTTP client with authentication headers."""
    with httpx.Client(base_url=BASE_URL) as client:
        client.headers["Authorization"] = f"Bearer {API_TOKEN}"
        yield client


def test_get_interactions_returns_200(client):
    """Test that GET /interactions/ returns HTTP 200."""
    response = client.get("/interactions/")
    assert response.status_code == 200


def test_get_interactions_response_is_a_list(client):
    """Test that GET /interactions/ response body is a JSON array."""
    response = client.get("/interactions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
