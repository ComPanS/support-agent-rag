## Stage 1 infrastructure

Start the local PostgreSQL/pgvector environment:

```bash
docker compose up -d
```

The database initializes tables and enables the `vector` extension from `infra/postgres/init.sql`. The current HTTP mock-shop API is deterministic and in-memory; it intentionally does not depend on the database yet. This keeps API behavior testable without Docker while making the persistence boundary explicit.

Available local API examples:

```bash
uv run uvicorn support_agent_rag:app --reload
curl http://127.0.0.1:8000/health
curl -H 'Authorization: Bearer client-token-alice' \\
  http://127.0.0.1:8000/shop/orders/order-1001
```

The mock shop exposes read access to an owned order and an operator-only return request. Customer ownership is enforced in the service layer, not in an LLM prompt.
