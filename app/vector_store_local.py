"""Helpers for creating and accessing the project's local Chroma vector store."""

import os
import re

import chromadb

DEFAULT_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
_BASE_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "ediva_knowledge")


def _slugify(value: str) -> str:
    """Convert provider/model names into safe collection name fragments."""
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "default"


def get_collection_name() -> str:
    """Build a collection name scoped to the active embedding configuration."""
    provider = _slugify(os.getenv("EMBEDDING_PROVIDER", "unknown"))

    if provider == "local":
        model = os.getenv("LOCAL_EMBEDDING_MODEL", "default")
    elif provider == "gemini":
        model = os.getenv("EMBEDDING_MODEL", "default")
    else:
        model = "default"

    return f"{_BASE_COLLECTION_NAME}__{provider}__{_slugify(model)}"


DEFAULT_COLLECTION_NAME = get_collection_name()


def get_chroma_client(persist_dir=DEFAULT_PERSIST_DIR):
    """Return a persistent Chroma client backed by the given directory."""
    return chromadb.PersistentClient(path=persist_dir)


def get_vector_store(persist_dir=DEFAULT_PERSIST_DIR):
    """Return the active Chroma collection, creating it if needed."""
    client = get_chroma_client(persist_dir)
    return client.get_or_create_collection(name=get_collection_name())
