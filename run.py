# Create virtual environment:
# python3 -m venv venv

# Activate virtual environment:
# source venv/bin/activate

# Deactivate virtual environment:
# deactivate

import os
from app import create_app
from app.gemini import generate_text
from scripts.ingest_to_chroma import ingest

app = create_app()


def run_startup_ingestion():
    """Load knowledge base to Chroma at runtime (not recommended for hosting)"""
    should_run = os.getenv("RUN_INGESTION", "false").lower() == "true"
    if not should_run:
        print("[INGEST] Skipped startup ingestion.")
        return

    try:
        print("[INGEST] Startup ingestion enabled. Beginning ingest_to_chroma...")
        ingest()
        print("[INGEST] Startup ingestion completed successfully.")
    except Exception as exc:
        print(f"[INGEST] Startup ingestion failed: {exc}")


if __name__ == "__main__":
    host = "0.0.0.0"
    port = int(os.getenv("PORT", "5050"))
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"

    # Print once from the serving process (avoid duplicate print from reloader parent).
    if not debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        print(f"[OK] Server running at http://{host}:{port}")
        try:
            startup_text = generate_text("Say 'Gemini connection OK' in 5 words.")
            print(f"[Gemini startup test] {startup_text}")
        except Exception as exc:
            print(f"[Gemini startup test failed] {exc}")
        run_startup_ingestion()

    app.run(host=host, port=port, debug=debug)

# Static knowledge → load_static_knowledge()
# Dynamic knowledge → get_video_knowledge_objects()
