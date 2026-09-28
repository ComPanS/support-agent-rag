import re
from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievedChunk:
    source: str
    section: str
    text: str
    score: float = 0.0


class KnowledgeBase:
    """Small deterministic lexical retriever used before embedding infrastructure."""

    def __init__(self, chunks: list[RetrievedChunk]) -> None:
        self.chunks = chunks

    def search(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        query_terms = _terms(query)
        scored = []
        for chunk in self.chunks:
            document_terms = _terms(chunk.text)
            overlap = query_terms & document_terms
            if not overlap:
                overlap = _expanded_overlap(query_terms, document_terms)
            if overlap:
                score = len(overlap) / max(len(query_terms), 1)
                scored.append(RetrievedChunk(chunk.source, chunk.section, chunk.text, score))
        return sorted(scored, key=lambda chunk: (-chunk.score, chunk.source))[:top_k]


def _expanded_overlap(query_terms: set[str], document_terms: set[str]) -> set[str]:
    """Match simple English inflections before embeddings are introduced."""
    matches = set()
    for query_term in query_terms:
        for document_term in document_terms:
            if len(query_term) >= 5 and len(document_term) >= 5:
                if query_term[:5] == document_term[:5]:
                    matches.add(document_term)
    return matches


def _terms(text: str) -> set[str]:
    words = re.findall(r"[a-zа-яё0-9]+", text.lower())
    stopwords = {"что", "как", "the", "is", "a", "an", "и", "в", "на", "у"}
    return set(words) - stopwords
