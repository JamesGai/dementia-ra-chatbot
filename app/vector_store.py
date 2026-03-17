"""Helpers for creating and accessing the project's Chroma vector store."""

import os

import chromadb
from chromadb.config import Settings

DEFAULT_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
DEFAULT_COLLECTION_NAME = "ediva_knowledge"


def get_chroma_client(persist_dir=DEFAULT_PERSIST_DIR):
    """Return a persistent Chroma client backed by the given directory."""
    return chromadb.PersistentClient(path=persist_dir)


def get_vector_store(persist_dir=DEFAULT_PERSIST_DIR):
    """Return the default Chroma collection, creating it if needed."""
    client = get_chroma_client(persist_dir)
    return client.get_or_create_collection(name=DEFAULT_COLLECTION_NAME)
