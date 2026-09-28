from dataclasses import dataclass

from .retriever import RetrievedChunk


@dataclass(frozen=True)
class GroundedAnswer:
    text: str
    citations: tuple[str, ...]
    grounded: bool


def compose_grounded_answer(query: str, chunks: list[RetrievedChunk]) -> GroundedAnswer:
    """Compose a deterministic context-only answer before adding an LLM."""
    del query
    if not chunks:
        return GroundedAnswer(
            "В базе знаний не найден подтверждённый ответ. Я могу передать вопрос оператору.",
            (),
            False,
        )
    citations = tuple(f"{chunk.source}#{chunk.section}" for chunk in chunks)
    text = " ".join(chunk.text for chunk in chunks)
    return GroundedAnswer(text, citations, True)
