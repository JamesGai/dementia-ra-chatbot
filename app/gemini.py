import os
from functools import lru_cache
from google import genai

DEFAULT_MODEL = "gemini-2.5-flash"

@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    api_key = (os.getenv("GEMINI_API_KEY") or "").strip()
    if not api_key:
        raise RuntimeError(
            "Missing GEMINI_API_KEY environment variable. "
            "Add it to a .env file or export it in your shell."
        )
    return genai.Client(api_key=api_key)


def generate_text(prompt: str, model: str = DEFAULT_MODEL) -> str:
    response = get_client().models.generate_content(model=model, contents=prompt)
    return (response.text or "").strip()
