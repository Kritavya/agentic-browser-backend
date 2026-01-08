"""
Health Endpoint Tests.

Tests the health check endpoint to ensure the application starts correctly.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_health_endpoint_returns_ok(client: TestClient) -> None:
    """Test that the health endpoint returns status ok."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_endpoint_is_fast(client: TestClient) -> None:
    """Test that the health endpoint responds quickly."""
    import time

    start = time.time()
    response = client.get("/health")
    duration_ms = (time.time() - start) * 1000

    assert response.status_code == 200
    assert duration_ms < 100, f"Health check took {duration_ms}ms, should be < 100ms"


def test_agent_run_endpoint_exists(client: TestClient) -> None:
    """Test that the agent run endpoint exists and accepts POST."""
    response = client.post(
        "/agent/run",
        json={"task": "Navigate to example.com"},
    )

    # Should return 200 with placeholder response
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert "status" in data


def test_session_create_endpoint_exists(client: TestClient) -> None:
    """Test that session create endpoint exists."""
    response = client.post("/session/create")

    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data


def test_session_list_endpoint_exists(client: TestClient) -> None:
    """Test that session list endpoint exists."""
    response = client.get("/session/")

    assert response.status_code == 200
    data = response.json()
    assert "sessions" in data
