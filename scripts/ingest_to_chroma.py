# python scripts/ingest_to_chroma.py

import sys
from pathlib import Path

# Allow running this file directly from the repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.static_knowledge_loader import load_static_knowledge
from app.video_service import get_video_knowledge_objects
from app.service_service import get_service_knowledge_objects
from app.embeddings import embed_text
from app.vector_store import get_vector_store, get_chroma_client

def sanitize_metadata(metadata: dict):
    """
    Ensure metadata only contains types supported by Chroma:
    str, int, float, bool, list, or None.
    Convert unsupported types (e.g., Firestore timestamps) to string.
    """
    clean = {}

    for key, value in metadata.items():
        if value is None:
            clean[key] = None
        elif isinstance(value, (str, int, float, bool)):
            clean[key] = value
        elif isinstance(value, list):
            # Ensure list elements are safe
            safe_list = []
            for item in value:
                if isinstance(item, (str, int, float, bool)):
                    safe_list.append(item)
                else:
                    safe_list.append(str(item))
            clean[key] = safe_list
        else:
            # Convert datetime, Firestore types, etc.
            clean[key] = str(value)

    return clean


def ingest(reset_collection=False):
    collection = get_vector_store()

    if reset_collection:
        print("[ingest] Resetting existing collection...")
        client = get_chroma_client()
        try:
            client.delete_collection(name="ediva_knowledge")
        except Exception:
            pass
        collection = client.get_or_create_collection(name="ediva_knowledge")

    print("[ingest] Loading static knowledge...")
    static_entries = load_static_knowledge()

    print("[ingest] Loading video knowledge...")
    video_entries = get_video_knowledge_objects()

    print("[ingest] Loading service knowledge...")
    service_entries = get_service_knowledge_objects()

    all_entries = static_entries + video_entries + service_entries

    print(f"[ingest] Total entries to process: {len(all_entries)}")

    ids = []
    docs = []
    metas = []
    embs = []

    for idx, entry in enumerate(all_entries, start=1):
        text = entry.get("content") or entry.get("semantic_text")

        if not text:
            continue

        print(f"[ingest] Embedding {idx}/{len(all_entries)}: {entry['id']}")

        vector = embed_text(text)

        raw_meta = {
            "page": str(entry.get("page", "")),
            "content_type": str(entry.get("content_type", "")),
            "source": str(entry.get("source", "")),
        }

        clean_meta = sanitize_metadata(raw_meta)

        ids.append(entry["id"])
        docs.append(text)
        metas.append(clean_meta)
        embs.append(vector)

    print("[ingest] Adding embeddings to Chroma...")

    collection.add(
        ids=ids,
        documents=docs,
        metadatas=metas,
        embeddings=embs
    )

    print(f"[ingest] Successfully added {len(ids)} vectors.")


if __name__ == "__main__":
    # Change to True if you want to wipe existing vectors before re-ingesting
    ingest(reset_collection=True)