# python scripts/test_vector_search.py

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.embeddings import embed_text
from app.vector_store import get_vector_store

def search(query, top_k=5):
    """Embed a query, run search in Chroma vector database, and print the top matches."""
    collection = get_vector_store()

    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    ids = results["ids"][0]
    docs = results["documents"][0]
    metas = results["metadatas"][0]

    for i in range(len(ids)):
        print("=" * 60)
        print("ID:", ids[i])
        print("Metadata:", metas[i])
        print("Preview:", docs[i][:200])

if __name__ == "__main__":
    search("How can I find dementia services near me?")
