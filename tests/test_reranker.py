import json

from support_agent_rag.rag.reranker import LocalReranker
from support_agent_rag.rag.retriever import RetrievedChunk


class StubResponse:
    def __init__(self, content: str) -> None:
        message = type("Message", (), {"content": content})()
        choice = type("Choice", (), {"message": message})()
        self.choices = [choice]


class StubCompletions:
    def __init__(self, content: str) -> None:
        self.content = content

    def create(self, **kwargs):
        return StubResponse(self.content)


class StubClient:
    def __init__(self, content: str) -> None:
        completions = StubCompletions(content)
        self.chat = type("Chat", (), {"completions": completions})()


def test_reranker_reorders_only_known_candidate_indices():
    chunks = [
        RetrievedChunk("a.md", "Other", "Delivery facts", 0.9),
        RetrievedChunk("b.md", "Returns", "Return policy", 0.4),
    ]
    ranking = {"ranking": [{"index": 1, "score": 0.95}, {"index": 0, "score": 0.1}]}
    client = StubClient(json.dumps(ranking))

    ranked = LocalReranker(client, "fake").rerank("return", chunks)

    assert [chunk.source for chunk in ranked] == ["b.md", "a.md"]
    assert ranked[0].score == 0.95


def test_reranker_falls_back_on_invalid_ranking():
    chunks = [
        RetrievedChunk("a.md", "Other", "Delivery facts", 0.9),
        RetrievedChunk("b.md", "Returns", "Return policy", 0.4),
    ]
    client = StubClient('{"ranking":[{"index":100,"score":1}]}')

    ranked = LocalReranker(client, "fake").rerank("return", chunks)

    assert [chunk.source for chunk in ranked] == ["a.md", "b.md"]
