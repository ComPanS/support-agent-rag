# Support Agent RAG

Backend-проект для AI-support агента интернет-магазина TechShop.

Агент будет отвечать по базе знаний, получать информацию о заказах и выполнять рискованные действия только после подтверждения оператора.

> Все данные в проекте синтетические. Реальные клиентские данные и реальные платёжные интеграции не используются.

## Status

| Stage | Status | Result |
|---|---|---|
| 0. Foundation | Done | Python package, `uv.lock`, Ruff, tests, CI |
| 1. Infrastructure and mock shop | Done | FastAPI, mock shop, auth boundary, PostgreSQL/pgvector Compose schema |
| 2. Persistence and seed data | Done | SQLAlchemy models, Alembic, database-backed reads, deterministic synthetic data |
| 3. RAG | In progress | Markdown ingestion, section-aware chunks, deterministic retrieval, citations |
| 4. Tools and policy | Planned | Typed tools, ownership and business rules |
| 5. LangGraph workflow | Planned | Routing, memory, escalation, human approval |

## Stage 2 persistence and seed data

The persistence substage adds SQLAlchemy models, an idempotent repository seed operation, and a CLI that writes deterministic synthetic data into PostgreSQL.

```bash
uv run python -m support_agent_rag.seed.cli --customers 50 --products 100 --orders 500
```

The command uses `DATABASE_URL` from the environment. Start PostgreSQL first:

```bash
docker compose up -d
export DATABASE_URL=postgresql+psycopg://support_agent:support_agent_dev@localhost:5432/support_agent
```


## Database migrations

The schema is managed by Alembic:

```bash
export DATABASE_URL=postgresql+psycopg://support_agent:support_agent_dev@localhost:5432/support_agent
uv run alembic upgrade head
uv run python -m support_agent_rag.seed.cli
```

Requirements: Python 3.12+, `uv`. Docker Desktop is required for PostgreSQL.

```bash
uv sync --locked
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

Run the API:

```bash
uv run uvicorn support_agent_rag:app --reload
```

Then check:

```bash
curl http://127.0.0.1:8000/health
curl -H 'Authorization: Bearer client-token-alice' \\
  http://127.0.0.1:8000/shop/orders/order-1001
```

Start local PostgreSQL with pgvector:

```bash
docker compose up -d
```

If Docker Desktop is not running, the API tests still work because the current mock shop uses an injected in-memory repository.

## Project decisions

### Why the project starts with a mock shop

The LLM is not needed to test ownership checks, order lookup, role permissions, or controlled errors. These rules are deterministic and must be tested independently of model behavior.

### Why authorization is in code

A prompt can be ignored or manipulated. The service layer receives the customer context and checks ownership before returning order data. The model can propose an action, but it cannot grant itself access.

### Why synthetic data

This is a portfolio project. Synthetic data makes local development reproducible and avoids exposing PII.

### Why RAG comes later

First we need stable domain operations and persistence boundaries. Otherwise it becomes difficult to distinguish a retrieval problem from an application or authorization problem.

## Implemented scope

- FastAPI application and `/health` endpoint;
- deterministic in-memory mock shop;
- client/operator role boundary;
- ownership check for order reads;
- operator-only return request;
- PostgreSQL + pgvector Compose definition;
- initial SQL tables;
- deterministic synthetic dataset generator.

Not implemented yet:

- Alembic migration workflow;
- database-backed repository;
- real authentication;
- LLM, embeddings, LangChain or LangGraph;
- production payment/logistics integrations.

## Verification

```text
8 passed
ruff check: passed
ruff format --check: passed
docker compose config --quiet: passed
```

One non-blocking warning comes from the current FastAPI/Starlette TestClient and its future HTTPX integration.

## License

MIT
