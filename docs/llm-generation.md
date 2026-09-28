# LLM answer generation

Retrieval and generation are separate concerns:

```text
question → retriever → evidence chunks → LLM → answer + source IDs
```

The generator accepts only the chunks returned by the retriever. When there are no chunks, it returns the existing refusal without making an LLM request.

## Provider configuration

Compatible with OpenAI Chat Completions API endpoints, including providers that expose the same interface.

```bash
OPENAI_API_KEY=...
OPENAI_BASE_URL=https://provider.example/v1  # optional
LLM_MODEL=provider/model-name
LLM_TIMEOUT_SECONDS=30
LLM_MAX_RETRIES=1
```

Keep real credentials in an untracked `.env` or secret manager. Never put keys into source, README examples, logs, or test fixtures.

## Output contract

The model must return JSON:

```json
{"answer":"...", "citations":["returns.md#Срок"]}
```

Application code validates JSON structure, non-empty answer, and citation membership against the actual evidence IDs. Invalid output falls back to a refusal. This prevents fabricated citations but does not prove each claim is entailed by the cited text; use a human-reviewed eval set for factual quality.

Tests use a stubbed client. They require no key and make no network requests.
