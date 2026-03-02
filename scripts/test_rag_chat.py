# python scripts/test_rag_chat.py

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.rag_service import generate_rag_answer

if __name__ == "__main__":
    while True:
        query = input("User: ")
        answer = generate_rag_answer(query)
        print("\nAssistant:", answer)
        print("\n" + "="*60 + "\n")