"""Helpers for creating and accessing the project's Chroma Cloud vector store."""

import os
import re

import chromadb

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


def get_chroma_client():
    """Return a Chroma Cloud client using environment variables."""
    api_key = os.getenv("CHROMA_API_KEY")
    tenant = os.getenv("CHROMA_TENANT")
    database = os.getenv("CHROMA_DATABASE")

    if not api_key:
        raise RuntimeError("Missing CHROMA_API_KEY for Chroma Cloud.")

    if tenant and database:
        return chromadb.CloudClient(
            api_key=api_key,
            tenant=tenant,
            database=database,
        )

    return chromadb.CloudClient(api_key=api_key)


def get_vector_store():
    """Return the active Chroma Cloud collection, creating it if needed."""
    client = get_chroma_client()
    return client.get_or_create_collection(name=get_collection_name())