"""Core package for the support-agent RAG service."""

from fastapi import FastAPI


def health() -> dict[str, str]:
    """Return the stable service health contract."""
    return {"service": "support-agent-rag", "status": "ok"}


def create_app() -> FastAPI:
    """Build the HTTP application without external service dependencies."""
    app = FastAPI(title="Support Agent RAG")

    @app.get("/health")
    def health_endpoint() -> dict[str, str]:
        return health()

    return app


app = create_app()
