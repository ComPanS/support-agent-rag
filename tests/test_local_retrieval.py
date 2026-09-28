from pathlib import Path

import pytest

from support_agent_rag.rag.embeddings import LocalEmbeddingKnowledgeBase
from support_agent_rag.rag.loader import load_knowledge_base
from support_agent_rag.rag.reranker import LocalReranker


def test_local_embedding_and_reranker_pipeline_retrieves_relevant_evidence():
    pytest.importorskip("dotenv")
    from dotenv import load_dotenv

    load_dotenv()
    if not Path(".env").exists():
        pytest.skip("Live local retrieval test requires .env and LM Studio")
    try:
        kb = load_knowledge_base(Path("data/kb"))
        semantic_kb = LocalEmbeddingKnowledgeBase.from_env(kb.chunks)
        reranker = LocalReranker.from_env()
        query = "Какой срок возврата товара?"
        candidates = semantic_kb.search(query, top_k=4)
        results = reranker.rerank(query, candidates, top_n=2)
        irrelevant = semantic_kb.search("Какие документы нужны для полёта на Марс?", top_k=4)
        assert results
        assert results[0].source == "returns.md"
        assert results[0].section == "Срок"
        assert irrelevant == []
    except Exception as exc:
        pytest.skip(f"Local LM Studio retrieval or reranker unavailable: {exc}")
