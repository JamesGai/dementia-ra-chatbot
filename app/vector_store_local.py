"""Helpers for creating and accessing the project's local Chroma vector store."""

import os

import chromadb

DEFAULT_COLLECTION_NAME = "iSupport_local"
DEFAULT_PERSIST_DIR = "./chroma_db"


def get_chroma_client(persist_dir=DEFAULT_PERSIST_DIR):
    """Return a persistent Chroma client backed by the given directory."""
    return chromadb.PersistentClient(path=persist_dir)


def get_vector_store(persist_dir=DEFAULT_PERSIST_DIR):
    """Return the active Chroma collection, creating it if needed."""
    client = get_chroma_client(persist_dir)
    return client.get_or_create_collection(name=DEFAULT_COLLECTION_NAME)
