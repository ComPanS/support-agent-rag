from dataclasses import dataclass

from support_agent_rag.llm.generation import OpenAICompatibleGenerator
from support_agent_rag.rag.retriever import RetrievedChunk


@dataclass
class StubMessage:
    content: str


@dataclass
class StubChoice:
    message: StubMessage


@dataclass
class StubResponse:
    choices: list[StubChoice]


class StubCompletions:
    def __init__(self, response: str):
        self.response = response
        self.request = None

    def create(self, **kwargs):
        self.request = kwargs
        return StubResponse([StubChoice(StubMessage(self.response))])


class StubClient:
    def __init__(self, response: str):
        completions = StubCompletions(response)
        self.completions = completions
        self.chat = type("Chat", (), {"completions": completions})()


def test_generation_receives_only_retrieved_evidence_and_returns_citation():
    client = StubClient('{"answer":"Возврат возможен 14 дней.","citations":["returns.md#Срок"]}')
    generator = OpenAICompatibleGenerator(client=client, model="fake-model")

    answer = generator.generate(
        "Сколько дней?",
        [RetrievedChunk("returns.md", "Срок", "Вернуть можно в течение 14 дней.", 0.8)],
    )

    assert answer.grounded is True
    assert answer.citations == ("returns.md#Срок",)
    assert client.completions.request is not None
    assert "Вернуть можно" in client.completions.request["messages"][1]["content"]


def test_generation_refuses_without_retrieved_context():
    client = StubClient('{"answer":"should not be used","citations":[]}')
    answer = OpenAICompatibleGenerator(client=client, model="fake-model").generate("question", [])

    assert answer.grounded is False
    assert answer.citations == ()
    assert client.completions.request is None


def test_generation_rejects_unknown_or_missing_citations():
    client = StubClient('{"answer":"Made up.","citations":["other.md#Nope"]}')
    answer = OpenAICompatibleGenerator(client=client, model="fake-model").generate(
        "question", [RetrievedChunk("returns.md", "Window", "14 days")]
    )

    assert answer.grounded is False
    assert answer.citations == ()
