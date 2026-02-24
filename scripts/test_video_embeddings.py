# python scripts/test_video_embeddings.py

from pathlib import Path
import sys

# Allow running this file directly from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.video_service import get_video_knowledge_objects
from app.embeddings import embed_text

videos = get_video_knowledge_objects()

for video in videos:
    print("=" * 60)
    print("ID:", video["id"])
    print("Title preview:", video["semantic_text"][:60], "...")

    embedding = embed_text(video["semantic_text"])

    print("Embedding length:", len(embedding))
    print("First 5 values:", embedding[:5])
