from app.embeddings import embed_text
from app.vector_store import get_vector_store
from app.gemini import generate_text


def retrieve(query: str, top_k: int = 5):
    """
    Embed query and retrieve top-k documents from Chroma.
    """
    collection = get_vector_store()

    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results["documents"][0], results["metadatas"][0]


def build_prompt(user_query: str, retrieved_chunks: list[str]) -> str:
    """
    Construct final prompt string to send to LLM.
    """

    context_block = "\n\n".join(
        [f"Context {i+1}:\n{chunk}" for i, chunk in enumerate(retrieved_chunks)]
    )

    system_instructions = """
You are an empathetic assistant supporting family carers of people with dementia.

Rules:
- Use ONLY the provided context.
- Do not provide medical diagnosis.
- If unsure, say you don't know.
- Maintain a supportive and compassionate tone.
- Provide practical guidance.
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
    """
    Full RAG pipeline:
    retrieve → build prompt → call Gemini
    """

    docs, metas = retrieve(user_query)

    prompt = build_prompt(user_query, docs)

    response = generate_text(prompt)

    return response