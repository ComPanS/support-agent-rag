from support_agent_rag.rag.answer import compose_grounded_answer
from support_agent_rag.rag.retriever import RetrievedChunk


def test_answer_is_grounded_and_contains_citations() -> None:
    answer = compose_grounded_answer(
        "How many days do I have for a return?",
        [RetrievedChunk("returns.md", "Window", "Returns are accepted within 14 days.", 0.8)],
    )

    assert "14 days" in answer.text
    assert "returns.md#Window" in answer.citations
    assert answer.grounded is True


def test_answer_refuses_when_context_is_missing() -> None:
    answer = compose_grounded_answer("What is the drone warranty?", [])

    assert answer.grounded is False
    assert "не найден" in answer.text.lower()
    assert answer.citations == ()
