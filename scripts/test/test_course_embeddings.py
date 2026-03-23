# python scripts/test/test_course_embeddings.py

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.course_service import get_course_knowledge_objects
from app.embeddings import embed_text

def main():
    """Generate and print embeddings for fetched course knowledge JSON objects."""
    courses = get_course_knowledge_objects()

    for course in courses:
        print("=" * 60)
        print("ID:", course["id"])
        print("Title preview:", course["semantic_text"][:60], "...")

        embedding = embed_text(course["semantic_text"])

        print("Embedding length:", len(embedding))
        print("First 5 values:", embedding[:5])

if __name__ == "__main__":
    main()
