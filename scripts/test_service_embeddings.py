# python scripts/test_service_embeddings.py

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.service_service import get_service_knowledge_objects
from app.embeddings import embed_text

def main():
    """Generate and print embeddings for fetched service knowledge JSON objects."""
    services = get_service_knowledge_objects()

    for service in services:
        print("=" * 60)
        print("ID:", service["id"])
        print("Title preview:", service["semantic_text"][:60], "...")

        embedding = embed_text(service["semantic_text"])

        print("Embedding length:", len(embedding))
        print("First 5 values:", embedding[:5])


if __name__ == "__main__":
    main()
