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
| 3. RAG | Done | Section-aware Markdown ingestion, lexical retrieval baseline, citations, refusal on empty context |
| 3a. LLM generation | In progress | OpenAI-compatible generation; output/citation validation |
| 4. Tools and policy | Planned | Typed tools, ownership and business rules |
| 5. LangGraph workflow | Planned | Routing, memory, escalation, human approval |

## Provider-compatible LLM generation

The RAG baseline can call an OpenAI-compatible chat completion endpoint:

```bash
export OPENAI_API_KEY=your-key
export OPENAI_BASE_URL=https://provider.example/v1  # optional for OpenAI-compatible hosts
export LLM_MODEL=provider/model-name
```

```python
from pathlib import Path
from support_agent_rag.llm import OpenAICompatibleGenerator
from support_agent_rag.rag.loader import load_knowledge_base

kb = load_knowledge_base(Path("data/kb"))
query = "Сколько дней даётся на возврат?"
chunks = kb.search(query)
answer = OpenAICompatibleGenerator.from_env().generate(query, chunks)
```

The generator is not called when retrieval is empty. Its output is accepted only when it is valid JSON, has a non-empty answer, and cites IDs that were actually supplied as evidence. This validates citation membership, not the factual entailment of every sentence; quality still needs evaluation.


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
- deterministic synthetic dataset generator;
- provider-compatible LLM answer generation over retrieved evidence, with validated source IDs.

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
