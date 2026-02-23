from flask import Blueprint, jsonify, request

from .gemini import generate_text

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return jsonify({"message": "Flask project is running"})


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

    print(f"[Gemini] Prompt: {prompt}\n[Gemini] Response: {text}")
    return jsonify({"response": text})
