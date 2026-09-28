from support_agent_rag import health


def test_health_returns_service_status() -> None:
    assert health() == {"service": "support-agent-rag", "status": "ok"}
