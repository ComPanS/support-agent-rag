# support-agent-rag

Stage 1: reproducible project foundation for a support-agent RAG service.

## Scope of stage 1

Stage 0 established the Python package, lockfile, quality checks, CI, and a smoke test. This stage adds the first executable service boundary: an HTTP health endpoint.

Included:
- installable Python package;
- FastAPI application factory;
- `/health` endpoint;
- API smoke test;
- reproducible dependency lockfile;
- CI quality gate.

Explicitly postponed:
- PostgreSQL and pgvector;
- Alembic migrations;
- synthetic shop data;
- mock shop operations;
- document ingestion and chunking;
- embeddings and vector database;
- LLM provider integration;
- support-channel adapters;
- authentication, persistence, and production deployment.

The health endpoint is intentionally small: it proves that the service can start and answer an HTTP request before external infrastructure and RAG components are introduced.

## Local development

```bash
uv sync --locked
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

## Stage 1 acceptance criteria

- A clean checkout installs with `uv sync --locked`.
- `GET /health` returns HTTP 200 and the stable service status JSON.
- Lint, formatting check, and tests pass.
- CI runs the same commands.
- No secrets or provider-specific code are required.

## Next stage

Stage 2 should add PostgreSQL/pgvector, migrations, deterministic synthetic shop data, and read-only mock-shop operations. RAG and LLM integration remain later stages.
