# python scripts/test/test_video_embeddings.py

from pathlib import Path
import sys

# Allow running this file directly by adding the repo root to sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.video_service import get_video_knowledge_objects
from app.embeddings import embed_text


def main():
    """Generate and print embeddings for fetched video knowledge JSON objects."""
    videos = get_video_knowledge_objects()

    for video in videos:
        print("=" * 60)
        print("ID:", video["id"])
        print("Title preview:", video["semantic_text"][:60], "...")

        embedding = embed_text(video["semantic_text"])

        print("Embedding length:", len(embedding))
        print("First 5 values:", embedding[:5])

if __name__ == "__main__":
    main()
