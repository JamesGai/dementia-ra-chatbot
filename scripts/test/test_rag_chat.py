# python scripts/test/test_rag_chat.py

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.rag_service import generate_rag_answer


def main():
    """Run a simple CLI loop to manually test RAG chat responses."""
    while True:
        query = input("User: ")
        if not query.strip():
            continue

        answer = generate_rag_answer(query)
        print("\nAssistant:", answer)
        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
