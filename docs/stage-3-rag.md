# Stage 3: RAG baseline

Implemented a deterministic retrieval baseline before adding an external embedding model or LLM.

## Flow

```text
Markdown knowledge base
  → section-aware chunks
  → lexical retrieval
  → grounded answer with source citations
```

## Why no LLM yet

This stage isolates retrieval quality from generation quality. If the retriever cannot find the correct source, adding an LLM only makes the answer sound more convincing; it does not fix the missing evidence.

The answer composer refuses to answer when no context is retrieved. This is the anti-hallucination contract that the future LLM prompt must preserve.

## Run the baseline

```python
from pathlib import Path
from support_agent_rag.rag.answer import compose_grounded_answer
from support_agent_rag.rag.loader import load_knowledge_base

kb = load_knowledge_base(Path("data/kb"))
chunks = kb.search("возврат 14 дней")
answer = compose_grounded_answer("Сколько дней даётся на возврат?", chunks)
```

The result contains answer text, citations such as `returns.md#Срок`, and a `grounded` flag.

## Next LLM-related step

Add a provider-neutral generation interface that receives only retrieved chunks, requires citations in structured output, and returns an explicit refusal when retrieval is empty. Provider credentials and model selection will stay outside the domain layer.
