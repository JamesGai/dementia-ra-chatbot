import os

from app import create_app
from app.gemini import generate_text

app = create_app()


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    debug = True

    # Print once from the serving process (avoid duplicate print from reloader parent).
    if not debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        print(f"[OK] Server running at http://{host}:{port}")
        try:
            startup_text = generate_text("Say 'Gemini connection OK' in 5 words.")
            print(f"[Gemini startup test] {startup_text}")
        except Exception as exc:
            print(f"[Gemini startup test failed] {exc}")

    app.run(host=host, port=port, debug=debug)
