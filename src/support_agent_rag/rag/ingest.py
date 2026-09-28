import re
from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentChunk:
    source: str
    section: str
    text: str


def chunk_markdown(source: str, markdown: str) -> list[DocumentChunk]:
    """Split Markdown into section-sized chunks while preserving citations."""
    chunks: list[DocumentChunk] = []
    section = "Document"
    buffer: list[str] = []
    for line in markdown.splitlines():
        heading = re.match(r"^##?\s+(.+)$", line)
        if heading:
            if buffer and " ".join(buffer).strip():
                chunks.append(DocumentChunk(source, section, " ".join(buffer).strip()))
            section = heading.group(1).strip()
            buffer = []
        elif line.strip():
            buffer.append(line.strip())
    if buffer:
        chunks.append(DocumentChunk(source, section, " ".join(buffer).strip()))
    return chunks
