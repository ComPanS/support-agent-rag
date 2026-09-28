from pathlib import Path

from support_agent_rag.rag.answer import compose_grounded_answer
from support_agent_rag.rag.loader import load_knowledge_base


def test_real_knowledge_base_answers_with_source() -> None:
    kb = load_knowledge_base(Path("data/kb"))
    result = compose_grounded_answer(
        "Сколько дней даётся на возврат?", kb.search("возврат 14 дней")
    )

    assert result.grounded is True
    assert "14 дней" in result.text
    assert any("returns.md" in citation for citation in result.citations)
