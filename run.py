# Create virtual environment:
# python3 -m venv venv

# Activate virtual environment:
# source venv/bin/activate

# Deactivate virtual environment:
# deactivate

import os

from app import create_app
from app.gemini import generate_text


def run_startup_checks():
    print("[OK] Initializing application...")

    try:
        startup_text = generate_text("Say 'Gemini connection OK' in 5 words.")
        print(f"[Gemini startup test] {startup_text}")
    except Exception as exc:
        print(f"[Gemini startup test failed] {exc}")


def run_startup_ingestion():
    should_run = os.getenv("RUN_INGESTION", "false").lower() == "true"
    if not should_run:
        print("[INGEST] Skipped startup ingestion.")
        return

    try:
        print("[INGEST] Running ingestion at startup...")
        from scripts.ingest_to_chroma import main as ingest_main

        ingest_main()
        print("[INGEST] Startup ingestion completed successfully.")
    except Exception as exc:
        print(f"[INGEST] Startup ingestion failed: {exc}")


# These run when Gunicorn imports run:app on Render
# run_startup_checks()
run_startup_ingestion()

app = create_app()


if __name__ == "__main__":
    host = "0.0.0.0"
    port = int(os.getenv("PORT", "5050"))
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"

    print(f"[OK] Server running at http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)

# Static knowledge → load_static_knowledge()
# Dynamic knowledge → get_video_knowledge_objects()
