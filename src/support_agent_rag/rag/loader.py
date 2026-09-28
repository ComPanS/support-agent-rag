from pathlib import Path

from .ingest import chunk_markdown
from .retriever import KnowledgeBase, RetrievedChunk


def load_knowledge_base(directory: Path) -> KnowledgeBase:
    chunks: list[RetrievedChunk] = []
    for path in sorted(directory.glob("*.md")):
        for chunk in chunk_markdown(path.name, path.read_text(encoding="utf-8")):
            chunks.append(RetrievedChunk(chunk.source, chunk.section, chunk.text))
    return KnowledgeBase(chunks)
