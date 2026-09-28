from pathlib import Path

from support_agent_rag.rag.embeddings import LocalEmbeddingKnowledgeBase
from support_agent_rag.rag.loader import load_knowledge_base


def test_live_local_embeddings_rank_relevant_russian_chunks_and_reject_noise():
    kb = load_knowledge_base(Path("data/kb"))
    semantic_kb = LocalEmbeddingKnowledgeBase.from_env(kb.chunks)

    queries = {
        "Какой срок возврата товара?": "returns.md",
        "Можно ли вернуть товар с нарушенной упаковкой?": "returns.md",
        "Сколько занимает доставка заказа?": "delivery.md",
        "Какие документы нужны для полёта на Марс?": None,
    }
    for query, expected_source in queries.items():
        results = semantic_kb.search(query, top_k=1)
        if expected_source is None:
            assert results == []
        else:
            assert results
            assert results[0].source == expected_source
            assert results[0].score >= semantic_kb.min_score
