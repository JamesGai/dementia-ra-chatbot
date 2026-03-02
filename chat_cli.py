import json
import sys
from urllib import error, request

DEFAULT_URL = "http://127.0.0.1:5000/api/gemini"
EXIT_WORDS = {"exit", "quit", ":q"}

def send_prompt(url: str, prompt: str) -> str:
    payload = json.dumps({"prompt": prompt}).encode("utf-8")
    req = request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return body.get("response", "")
    except error.HTTPError as exc:
        try:
            body = json.loads(exc.read().decode("utf-8"))
            msg = body.get("error") or str(exc)
        except Exception:
            msg = str(exc)
        raise RuntimeError(f"Server returned error: {msg}") from exc
    except error.URLError as exc:
        raise RuntimeError(
            "Cannot reach server. Make sure run.py is running at "
            f"{url.rsplit('/api/gemini', 1)[0]}"
        ) from exc


def main() -> int:
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL

    print(f"Chat CLI connected to: {url}")
    print("Type your message and press Enter. Type 'exit' to quit.\n")

    while True:
        try:
            prompt = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting chat.")
            return 0

        if not prompt:
            continue
        if prompt.lower() in EXIT_WORDS:
            print("Exiting chat.")
            return 0

        try:
            response_text = send_prompt(url, prompt)
        except Exception as exc:
            print(f"Error: {exc}\n")
            continue

        print(f"Bot: {response_text}\n")


if __name__ == "__main__":
    raise SystemExit(main())
