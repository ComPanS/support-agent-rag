from fastapi.testclient import TestClient

from support_agent_rag import app, health


def test_health_returns_service_status() -> None:
    assert health() == {"service": "support-agent-rag", "status": "ok"}


def test_health_endpoint_returns_service_status() -> None:
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"service": "support-agent-rag", "status": "ok"}
