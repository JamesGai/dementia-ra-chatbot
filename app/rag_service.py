import os

from app.embeddings import embed_text
from app.gemini import generate_text
from app.vector_store_local import get_vector_store as get_vector_store_local
from app.vector_store_cloud import get_vector_store as get_vector_store_cloud


def retrieve(query: str, top_k: int = 5):
    """Embed query text and retrieve top-k documents from Chroma."""
    collection_type = os.getenv("COLLECTION_TYPE", "cloud").strip().lower()
    collection = (
        get_vector_store_local()
        if collection_type == "local"
        else get_vector_store_cloud()
    )
    print ("++++++++++++++ Vector DB type: ", collection_type, "++++++++++++++")
    print ("++++++++++++++ Vector DB collection: ", collection, "++++++++++++++")
    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    return results["documents"][0], results["metadatas"][0]


def build_prompt(user_query: str, retrieved_chunks: list[str]) -> str:
    """Build the final context-grounded prompt for generation."""
    context_block = "\n\n".join(
        [f"Context {i + 1}:\n{chunk}" for i, chunk in enumerate(retrieved_chunks)]
    )

    system_instructions = """
You are an empathetic assistant supporting family carers of people with dementia.

Rules:
- Use ONLY the provided context.
- Do not provide medical diagnosis.
- If unsure, say you don't know.
- Maintain a supportive and compassionate tone.
- Provide practical guidance.
- Keep answers short and easy to read on a mobile phone.
- Use plain English and short sentences.
- Prefer 2 to 4 short sentences.
- Keep the full answer under 60 words unless the user clearly asks for more detail.
- Focus on the single most useful answer first.
- If steps are needed, use at most 3 short bullet points.
- Do not write long paragraphs.
"""

    prompt = f"""
{system_instructions}

{context_block}

User Question:
{user_query}

Answer:
"""

    return prompt.strip()


def generate_rag_answer(user_query: str) -> str:
    """Run the RAG pipeline: retrieve context, build prompt, and generate output."""
    docs, _ = retrieve(user_query)
    prompt = build_prompt(user_query, docs)
    return generate_text(prompt)
