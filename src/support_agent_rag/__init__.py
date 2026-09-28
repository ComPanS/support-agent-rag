"""Core package for the support-agent RAG service."""


def health() -> dict[str, str]:
    """Return the stable service health contract."""
    return {"service": "support-agent-rag", "status": "ok"}
