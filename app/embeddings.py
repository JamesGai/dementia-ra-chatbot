import os
from pathlib import Path
from google import genai
from dotenv import load_dotenv

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Ensure environment variables are available when scripts run directly.
load_dotenv(PROJECT_ROOT / ".env")


def get_embedding_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY")
    return genai.Client(api_key=api_key)


def embed_text(text: str):
    client = get_embedding_client()

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )

    # Support both older and newer SDK response shapes.
    if hasattr(response, "embedding") and response.embedding is not None:
        return response.embedding
    if hasattr(response, "embeddings") and response.embeddings:
        first = response.embeddings[0]
        if hasattr(first, "values"):
            return first.values
        return first
    raise RuntimeError("Unexpected embedding response format")
