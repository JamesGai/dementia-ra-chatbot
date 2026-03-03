from flask import Blueprint, jsonify, request

from .gemini import generate_text
from .rag_service import generate_rag_answer

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return jsonify({"message": "Flask project is running"})


# 🔹 Keep this for raw Gemini testing
@bp.post("/api/gemini")
def gemini():
    payload = request.get_json(silent=True) or {}
    prompt = (payload.get("prompt") or "").strip()
    if not prompt:
        return jsonify({"error": "Please provide 'prompt' in JSON body."}), 400

    try:
        text = generate_text(prompt)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500

    return jsonify({"response": text})


# 🔥 NEW: RAG Chat Endpoint
@bp.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    user_message = (payload.get("message") or "").strip()

    if not user_message:
        return jsonify({"error": "Please provide 'message' in JSON body."}), 400

    try:
        answer = generate_rag_answer(user_message)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500

    print(f"[RAG] User: {user_message}")
    print(f"[RAG] Assistant: {answer}")

    return jsonify({"response": answer})