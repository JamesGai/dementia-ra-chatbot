from flask import Blueprint, jsonify, request

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return jsonify({"message": "Flask project is running"})


# Raw Gemini testing
@bp.post("/api/gemini")
def gemini():
    from .gemini import generate_text

    payload = request.get_json(silent=True) or {}
    prompt = (payload.get("prompt") or "").strip()
    if not prompt:
        return jsonify({"error": "Please provide 'prompt' in JSON body."}), 400

    try:
        text = generate_text(prompt)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500

    return jsonify({"response": text})


# RAG Chat Endpoint
@bp.post("/api/chat")
def chat():
    from .rag_service import generate_rag_answer

    payload = request.get_json(silent=True) or {}
    prompt = (payload.get("prompt") or "").strip()

    if not prompt:
        return jsonify({"error": "Please provide 'prompt' in JSON body."}), 400

    try:
        answer = generate_rag_answer(prompt)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500

    print(f"[RAG] User: {prompt}")
    print(f"[RAG] Assistant: {answer}")

    return jsonify({"response": answer})
