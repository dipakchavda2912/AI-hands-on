"""
Integration tests for API server.

Run with: pytest tests/test_api_integration.py -v
"""

import pytest
from fastapi.testclient import TestClient
from api_server import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["version"] == "3.0.0"


def test_agent_run_endpoint(client):
    """Test agent run endpoint."""
    payload = {
        "request": "Test request",
        "thread_id": "test_123"
    }

    response = client.post("/agent/run", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "thread_id" in data
    assert "execution_time" in data


def test_agent_run_invalid_request(client):
    """Test agent run with invalid request."""
    payload = {
        "request": "",  # Empty request should fail validation
    }

    response = client.post("/agent/run", json=payload)
    assert response.status_code == 422  # Validation error


def test_background_endpoint(client):
    """Test background execution endpoint."""
    payload = {
        "request": "Background task"
    }

    response = client.post("/agent/background", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "queued"
