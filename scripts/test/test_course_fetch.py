# python scripts/test/test_course_fetch.py

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.course_service import get_course_knowledge_objects

def main():
    """Fetch and print transformed course knowledge JSON objects."""
    courses = get_course_knowledge_objects()

    for course in courses:
        print("=" * 50)
        print(course["id"])
        print(course["semantic_text"])

if __name__ == "__main__":
    main()
