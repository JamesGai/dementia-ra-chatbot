import chromadb
from chromadb.config import Settings

def get_chroma_client(persist_dir="./chroma_db"):
    return chromadb.Client(
        Settings(
            persist_directory=persist_dir,
            anonymized_telemetry=False,
        )
    )

def get_vector_store(persist_dir="./chroma_db"):
    client = get_chroma_client(persist_dir)
    return client.get_or_create_collection(name="ediva_knowledge")