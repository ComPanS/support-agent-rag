# support-agent-rag

Stage 1: reproducible project foundation for a support-agent RAG service.

## Scope of stage 1

Included:
- installable Python package;
- typed, minimal health-check contract;
- pytest smoke test;
- Ruff linting and formatting;
- reproducible dependency lockfile;
- CI quality gate.

Explicitly postponed:
- document ingestion and chunking;
- embeddings and vector database;
- LLM provider integration;
- support-channel adapters;
- authentication, persistence, and production deployment.

The health check is intentionally small: it proves that the package can be imported and executed before expensive RAG components are introduced.

## Local development

```bash
uv sync --locked
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

## Stage 1 acceptance criteria

- A clean checkout installs with `uv sync --locked`.
- Lint, formatting check, and tests pass.
- CI runs the same commands.
- No secrets or provider-specific code are required.

## Next stage

Stage 2 should define the domain contracts for support documents, retrieved passages, and answer citations, with tests before implementation.
