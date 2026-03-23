# python scripts/pdf_chunking.py

"""Split extracted PDF text into searchable chunks with metadata."""

import argparse
import re
from pathlib import Path

from pdf_extraction import extract_pdf_pages


def split_into_paragraphs(text: str) -> list[str]:
    """
    Split text into paragraph-like blocks.
    PDF text often breaks lines unnaturally, so this groups lines into larger units.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return []

    paragraphs = []
    current = []

    for line in lines:
        current.append(line)

        # Treat punctuation as a soft paragraph boundary
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
    """
    Merge paragraph blocks into chunks up to max_chars.
    Adds overlap between chunks for continuity.
    """
    if not paragraphs:
        return []

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        # If one paragraph is too long, split it directly
        if len(paragraph) > max_chars:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""

            start = 0
            step = max_chars - overlap_chars
            while start < len(paragraph):
                end = start + max_chars
                chunk = paragraph[start:end].strip()
                if chunk:
                    chunks.append(chunk)
                start += step
            continue

        proposed = (
            f"{current_chunk}\n\n{paragraph}".strip()
            if current_chunk
            else paragraph
        )

        if len(proposed) <= max_chars:
            current_chunk = proposed
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())

                overlap_text = current_chunk[-overlap_chars:].strip()
                current_chunk = f"{overlap_text}\n\n{paragraph}".strip()
            else:
                current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def build_pdf_chunks(
    pages: list[dict],
    document_title: str,
    source: str = "pdf_manual",
    max_chars: int = 1200,
    overlap_chars: int = 200,
) -> list[dict]:
    """
    Convert extracted page text into chunk objects with metadata.
    """
    all_chunks = []

    for page_data in pages:
        page_number = page_data["page"]
        text = page_data["text"].strip()

        if not text:
            continue

        paragraphs = split_into_paragraphs(text)
        page_chunks = chunk_paragraphs(
            paragraphs=paragraphs,
            max_chars=max_chars,
            overlap_chars=overlap_chars,
        )

        for chunk_index, chunk_text in enumerate(page_chunks, start=1):
            chunk_id = f"pdf_p{page_number}_c{chunk_index}"

            all_chunks.append(
                {
                    "id": chunk_id,
                    "text": chunk_text,
                    "metadata": {
                        "source": source,
                        "document_title": document_title,
                        "page": page_number,
                        "chunk_index": chunk_index,
                    },
                }
            )

    return all_chunks


def print_chunk_preview(chunks: list[dict], limit: int = 5) -> None:
    print(f"\nTotal chunks created: {len(chunks)}")

    for chunk in chunks[:limit]:
        print(f"\n{'=' * 20} {chunk['id']} {'=' * 20}")
        print("Metadata:", chunk["metadata"])
        print("Text preview:")
        print(chunk["text"][:700])
        if len(chunk["text"]) > 700:
            print("...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Chunk PDF text into retrieval-friendly chunks with metadata."
    )
    parser.add_argument(
        "pdf_path",
        nargs="?",
        default="data/iSupport NZ.pdf",
        help="Path to the PDF file.",
    )
    parser.add_argument(
        "--document-title",
        default="iSupport NZ",
        help="Document title to store in chunk metadata.",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=1200,
        help="Maximum characters per chunk.",
    )
    parser.add_argument(
        "--overlap-chars",
        type=int,
        default=200,
        help="Character overlap between consecutive chunks.",
    )
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path)

    pages = extract_pdf_pages(str(pdf_path))
    chunks = build_pdf_chunks(
        pages=pages,
        document_title=args.document_title,
        max_chars=args.max_chars,
        overlap_chars=args.overlap_chars,
    )

    print_chunk_preview(chunks)