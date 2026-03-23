# python scripts/ingest_to_chroma_cloud.py

"""Ingest static + Firestore knowledge into the Chroma Cloud collection."""

import argparse
import sys
from pathlib import Path
from typing import Any

from chromadb.errors import InvalidArgumentError

# Allow running this file directly from the repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.static_knowledge_loader import load_static_knowledge
from app.video_service import get_video_knowledge_objects
from app.course_service import get_course_knowledge_objects
from app.service_service import get_service_knowledge_objects
from app.pdf_service import get_pdf_knowledge_objects
from app.embeddings import embed_text
from app.vector_store_cloud import (
    DEFAULT_COLLECTION_NAME,
    get_chroma_client,
    get_vector_store,
)


def sanitize_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    """
    Ensure metadata only contains types supported by Chroma:
    str, int, float, bool, list, or None.
    Convert unsupported types (e.g., Firestore timestamps) to string.
    """
    clean: dict[str, Any] = {}

    for key, value in metadata.items():
        if value is None:
            clean[key] = None
        elif isinstance(value, (str, int, float, bool)):
            clean[key] = value
        elif isinstance(value, list):
            safe_list = []
            for item in value:
                if isinstance(item, (str, int, float, bool)):
                    safe_list.append(item)
                else:
                    safe_list.append(str(item))
            clean[key] = safe_list
        else:
            clean[key] = str(value)

    return clean


def _reset_collection() -> None:
    """Delete and recreate the target Chroma Cloud collection if it exists."""
    print("[ingest-cloud] Resetting existing collection...")
    client = get_chroma_client()
    try:
        client.delete_collection(name=DEFAULT_COLLECTION_NAME)
    except Exception:
        # Collection may not exist yet; safe to continue.
        pass


def ingest(reset_collection: bool = False) -> None:
    """Load all knowledge sources, embed entries, and store them in Chroma Cloud."""
    collection = get_vector_store()

    if reset_collection:
        _reset_collection()
        collection = get_vector_store()

    print("[ingest-cloud] Loading static knowledge...")
    static_entries = load_static_knowledge()

    print("[ingest-cloud] Loading video knowledge...")
    video_entries = get_video_knowledge_objects()

    print("[ingest-cloud] Loading course knowledge...")
    course_entries = get_course_knowledge_objects()

    print("[ingest-cloud] Loading service knowledge...")
    service_entries = get_service_knowledge_objects()

    print("[ingest-cloud] Loading PDF knowledge...")
    pdf_entries = get_pdf_knowledge_objects()

    all_entries = (
        static_entries
        + video_entries
        + course_entries
        + service_entries
        + pdf_entries
    )

    print(f"[ingest-cloud] Total entries to process: {len(all_entries)}")

    ids = []
    docs = []
    metas = []
    embs = []

    for idx, entry in enumerate(all_entries, start=1):
        entry_id = entry.get("id")
        text = entry.get("content") or entry.get("semantic_text")

        if not entry_id or not text:
            print(f"[ingest-cloud] Skipping {idx}/{len(all_entries)}: missing id/text")
            continue

        print(f"[ingest-cloud] Embedding {idx}/{len(all_entries)}: {entry_id}")

        vector = embed_text(text)

        raw_meta = {
            "page": str(entry.get("page", "")),
            "content_type": str(entry.get("content_type", "")),
            "source": str(entry.get("source", "")),
        }

        clean_meta = sanitize_metadata(raw_meta)

        ids.append(entry_id)
        docs.append(text)
        metas.append(clean_meta)
        embs.append(vector)

    if not ids:
        print("[ingest-cloud] No valid entries to add. Ingest finished with 0 vectors.")
        return

    print("[ingest-cloud] Upserting embeddings to Chroma Cloud...")
    try:
        collection.upsert(
            ids=ids,
            documents=docs,
            metadatas=metas,
            embeddings=embs,
        )
    except InvalidArgumentError as exc:
        raise RuntimeError(
            "[ingest-cloud] Chroma rejected the embeddings, usually because this "
            f"collection was created with a different embedding dimension. "
            f"Active collection: '{DEFAULT_COLLECTION_NAME}'. "
            "Re-run with '--reset' to rebuild the active collection."
        ) from exc

    print(f"[ingest-cloud] Successfully upserted {len(ids)} vectors.")


def _parse_args() -> argparse.Namespace:
    """Parse CLI options for ingestion."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete and recreate the collection before ingestion.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    ingest(reset_collection=args.reset)
