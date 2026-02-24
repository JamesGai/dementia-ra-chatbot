# python scripts/test_service_fetch.py

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.service_service import get_service_knowledge_objects

def main():
    """Fetch and print transformed service knowledge JSON objects."""
    services = get_service_knowledge_objects()

    for service in services:
        print("=" * 50)
        print(service["id"])
        print(service["semantic_text"])

if __name__ == "__main__":
    main()
