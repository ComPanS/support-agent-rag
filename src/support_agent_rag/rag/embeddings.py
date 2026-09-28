import os

from openai import OpenAI

from .retriever import RetrievedChunk


class LocalEmbeddingKnowledgeBase:
    """Embed documents and queries via the LM Studio OpenAI-compatible API."""

    def __init__(
        self,
        chunks: list[RetrievedChunk],
        client: OpenAI,
        model: str,
        min_score: float | None = None,
    ) -> None:
        self.chunks = chunks
        self.client = client
        self.model = model
        self.min_score = (
            min_score if min_score is not None else float(os.getenv("EMBEDDING_MIN_SCORE", "0.50"))
        )
        self._vectors = self._embed([chunk.text for chunk in chunks]) if chunks else []

    @classmethod
    def from_env(cls, chunks: list[RetrievedChunk]) -> "LocalEmbeddingKnowledgeBase":
        base_url = os.getenv("EMBEDDING_BASE_URL", "http://localhost:1234/v1")
        model = os.getenv("EMBEDDING_MODEL", "text-embedding-qwen3-embedding-0.6b")
        client = OpenAI(
            api_key=os.getenv("EMBEDDING_API_KEY", "lm-studio"),
            base_url=base_url,
            timeout=float(os.getenv("EMBEDDING_TIMEOUT_SECONDS", "60")),
            max_retries=1,
        )
        return cls(chunks, client, model)

    def search(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        if not self.chunks or top_k <= 0:
            return []
        query_vector = self._embed([query])[0]
        ranked = [
            (self._cosine(query_vector, vector), chunk)
            for chunk, vector in zip(self.chunks, self._vectors, strict=True)
        ]
        matches = [
            RetrievedChunk(chunk.source, chunk.section, chunk.text, score)
            for score, chunk in ranked
            if score >= self.min_score
        ]
        return sorted(matches, key=lambda chunk: (-chunk.score, chunk.source))[:top_k]

    def _embed(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embeddings.create(model=self.model, input=texts)
        ordered = sorted(response.data, key=lambda item: item.index)
        return [item.embedding for item in ordered]

    @staticmethod
    def _cosine(left: list[float], right: list[float]) -> float:
        dot = sum(a * b for a, b in zip(left, right, strict=True))
        left_norm = sum(value * value for value in left) ** 0.5
        right_norm = sum(value * value for value in right) ** 0.5
        if not left_norm or not right_norm:
            return 0.0
        return dot / (left_norm * right_norm)
