"""Helpers for creating and accessing the project's Chroma Cloud vector store."""

import os

import chromadb

DEFAULT_COLLECTION_NAME = "iSupport_cloud"


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
    return client.get_or_create_collection(name=DEFAULT_COLLECTION_NAME)