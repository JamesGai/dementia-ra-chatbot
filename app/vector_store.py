"""Helpers for creating and accessing the project's Chroma vector store."""

import chromadb
from chromadb.config import Settings

DEFAULT_PERSIST_DIR = "./chroma_db"
DEFAULT_COLLECTION_NAME = "ediva_knowledge"

def get_chroma_client(persist_dir: str = DEFAULT_PERSIST_DIR):
    """Return a configured Chroma client with local persistence enabled."""
    return chromadb.Client(
        Settings(
            persist_directory=persist_dir,
            anonymized_telemetry=False,
        )
    )

def get_vector_store(
    persist_dir: str = DEFAULT_PERSIST_DIR,
    collection_name: str = DEFAULT_COLLECTION_NAME,
):
    """Return the existing collection or create it when missing."""
    client = get_chroma_client(persist_dir)
    return client.get_or_create_collection(name=collection_name)
