# python scripts/test_video_fetch.py

from pathlib import Path
import sys

# Allow running this file directly from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.video_service import get_video_knowledge_objects

def main():
    """Fetch and print transformed video knowledge JSON objects."""
    videos = get_video_knowledge_objects()

    for video in videos:
        print("=" * 50)
        print(video["id"])
        print(video["semantic_text"])

if __name__ == "__main__":
    main()
