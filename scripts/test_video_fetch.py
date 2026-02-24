# python scripts/test_video_fetch.py
from pathlib import Path
import sys

# Allow running this file directly from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.video_service import get_video_knowledge_objects

videos = get_video_knowledge_objects()

for v in videos:
    print("=" * 50)
    print(v["id"])
    print(v["semantic_text"])
