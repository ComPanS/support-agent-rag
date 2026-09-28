import json
import sys
from pathlib import Path

from dotenv import load_dotenv

from support_agent_rag.llm.generation import OpenAICompatibleGenerator
from support_agent_rag.rag.loader import load_knowledge_base


def main() -> None:
    load_dotenv()
    generator = OpenAICompatibleGenerator.from_env()
    knowledge_base = load_knowledge_base(Path("data/kb"))
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        raise SystemExit('Usage: uv run python -m support_agent_rag.llm.smoke "your question"')
    chunks = knowledge_base.search(question, top_k=4)
    answer = generator.generate(question, chunks)
    print(
        json.dumps(
            {
                "answer": answer.text,
                "citations": answer.citations,
                "grounded": answer.grounded,
                "retrieved_chunks": len(chunks),
                "model": generator.model,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
