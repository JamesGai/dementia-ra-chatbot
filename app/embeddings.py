import os
from pathlib import Path
from google import genai
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Ensure environment variables are available when scripts run directly.
load_dotenv(PROJECT_ROOT / ".env")

EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER").lower()
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
LOCAL_EMBEDDING_MODEL = os.getenv("LOCAL_EMBEDDING_MODEL")

_local_model = None

def get_embedding_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY")
    return genai.Client(api_key=api_key)


def _embed_text_gemini(text: str):
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


def _get_local_model():
    global _local_model
    if _local_model is not None:
        return _local_model

    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError(
            "Local embeddings require sentence-transformers. "
            "Install it with: pip install sentence-transformers"
        ) from exc

    _local_model = SentenceTransformer(LOCAL_EMBEDDING_MODEL)
    return _local_model


def _embed_text_local(text: str):
    model = _get_local_model()
    vector = model.encode(text, normalize_embeddings=True)
    if hasattr(vector, "tolist"):
        return vector.tolist()
    return vector


def embed_text(text: str):
    if EMBEDDING_PROVIDER == "local":
        return _embed_text_local(text)
    if EMBEDDING_PROVIDER == "gemini":
        return _embed_text_gemini(text)
    raise RuntimeError(
        f"Unsupported EMBEDDING_PROVIDER='{EMBEDDING_PROVIDER}'. "
        "Use 'gemini' or 'local'."
    )
