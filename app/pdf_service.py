from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import fitz

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DEFAULT_SOURCE = "pdf_document"


def _clean_text(text: str) -> str:
    """Normalize PDF text by trimming lines and removing empty rows."""
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())


def extract_pdf_pages(pdf_path: str | Path) -> list[dict[str, Any]]:
    """Read a PDF and return cleaned text for each page."""
    document = fitz.open(pdf_path)
    pages: list[dict[str, Any]] = []

    try:
        for index, page in enumerate(document, start=1):
            pages.append(
                {
                    "page": index,
                    "text": _clean_text(page.get_text("text")),
                }
            )
    finally:
        document.close()

    return pages


def split_into_paragraphs(text: str) -> list[str]:
    """Group PDF lines into paragraph-like blocks for chunking."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return []

    paragraphs: list[str] = []
    current: list[str] = []

    for line in lines:
        current.append(line)
        if re.search(r"[.!?:]$", line):
            paragraphs.append(" ".join(current).strip())
            current = []

    if current:
        paragraphs.append(" ".join(current).strip())

    return paragraphs


def chunk_paragraphs(
    paragraphs: list[str],
    max_chars: int = 1200,
    overlap_chars: int = 200,
) -> list[str]:
    """Merge paragraphs into embedding-sized chunks with overlap."""
    if not paragraphs:
        return []

    chunks: list[str] = []
    current_chunk = ""
    step = max_chars - overlap_chars

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        if len(paragraph) > max_chars:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""

            start = 0
            while start < len(paragraph):
                chunk = paragraph[start:start + max_chars].strip()
                if chunk:
                    chunks.append(chunk)
                start += step
            continue

        proposed = f"{current_chunk}\n\n{paragraph}".strip() if current_chunk else paragraph
        if len(proposed) <= max_chars:
            current_chunk = proposed
            continue

        if current_chunk:
            chunks.append(current_chunk.strip())
            overlap_text = current_chunk[-overlap_chars:].strip()
            current_chunk = f"{overlap_text}\n\n{paragraph}".strip()
        else:
            current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def _slugify(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return normalized or "pdf"


def build_pdf_knowledge_objects(
    pages: list[dict[str, Any]],
    document_title: str,
    source: str | None = None,
    max_chars: int = 1200,
    overlap_chars: int = 200,
) -> list[dict[str, Any]]:
    """Convert extracted pages into knowledge objects ready for embedding."""
    entries: list[dict[str, Any]] = []
    document_slug = _slugify(document_title)
    document_source = source or document_title

    for page_data in pages:
        page_number = page_data["page"]
        text = page_data["text"].strip()
        if not text:
            continue

        page_chunks = chunk_paragraphs(
            split_into_paragraphs(text),
            max_chars=max_chars,
            overlap_chars=overlap_chars,
        )

        for chunk_index, chunk_text in enumerate(page_chunks, start=1):
            entries.append(
                {
                    "id": f"pdf_{document_slug}_p{page_number}_c{chunk_index}",
                    "page": document_slug,
                    "section": "pdf_content",
                    "source": document_source,
                    "content_type": "document_chunk",
                    "title": f"{document_title} Page {page_number}",
                    "content": chunk_text,
                    "document_title": document_title,
                    "document_type": "pdf",
                    "chunk_index": chunk_index,
                    "page_number": page_number,
                }
            )

    return entries


def get_pdf_knowledge_objects(data_dir: str | Path = DATA_DIR) -> list[dict[str, Any]]:
    """Load all PDFs from the data directory as embedding-ready knowledge objects."""
    root = Path(data_dir)
    pdf_paths = sorted(root.glob("*.pdf"))
    entries: list[dict[str, Any]] = []

    for pdf_path in pdf_paths:
        document_title = pdf_path.stem
        pages = extract_pdf_pages(pdf_path)
        entries.extend(
            build_pdf_knowledge_objects(
                pages=pages,
                document_title=document_title,
                source=document_title,
            )
        )

    return entries
