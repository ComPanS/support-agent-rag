from support_agent_rag.rag.ingest import chunk_markdown
from support_agent_rag.rag.retriever import KnowledgeBase, RetrievedChunk


def test_markdown_is_chunked_with_source_metadata() -> None:
    chunks = chunk_markdown(
        "returns.md",
        "# Returns\n\n## Window\n\nYou can return an item within 14 days.\n\n"
        "## Exclusions\n\nOpened software cannot be returned.",
    )

    assert len(chunks) == 2
    assert chunks[0].source == "returns.md"
    assert chunks[0].section == "Window"
    assert "14 days" in chunks[0].text


def test_knowledge_base_retrieves_relevant_chunks_and_sources() -> None:
    kb = KnowledgeBase(
        [
            RetrievedChunk("returns.md", "Window", "Returns are accepted within 14 days."),
            RetrievedChunk("delivery.md", "Speed", "Delivery takes 2 business days."),
        ]
    )

    results = kb.search("How long can I return an item?", top_k=1)

    assert len(results) == 1
    assert results[0].source == "returns.md"
    assert results[0].score > 0


def test_empty_retrieval_is_explicit() -> None:
    kb = KnowledgeBase(
        [RetrievedChunk("returns.md", "Window", "Returns are accepted within 14 days.")]
    )

    assert kb.search("What is the warranty for a drone?", top_k=3) == []
