# python scripts/pdf_extraction.py

"""Read the PDF and turn it into clean raw text page by page."""

import argparse

import fitz  # PyMuPDF


def extract_pdf_pages(pdf_path: str) -> list[dict]:
    doc = fitz.open(pdf_path)
    pages = []

    for i, page in enumerate(doc):
        text = page.get_text("text")
        cleaned = "\n".join(
            line.strip() for line in text.splitlines() if line.strip()
        )

        pages.append({
            "page": i + 1,
            "text": cleaned
        })

    doc.close()
    return pages


def print_extracted_pages(pages: list[dict]) -> None:
    for page in pages:
        print(f"\n{'=' * 20} Page {page['page']} {'=' * 20}")
        print(page["text"] or "[No text extracted from this page]")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract and display text from a PDF file page by page."
    )
    parser.add_argument(
        "pdf_path",
        nargs="?",
        default="data/iSupport NZ.pdf",
        help="Path to the PDF file to extract text from.",
    )
    args = parser.parse_args()

    pdf_path = args.pdf_path
    pages = extract_pdf_pages(pdf_path)

    print(f"Extracted {len(pages)} pages")
    print_extracted_pages(pages)
