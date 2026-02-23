# Flask Starter

Minimal Flask project scaffold.

## Project structure

```text
.
├── app
│   ├── __init__.py
│   └── routes.py
├── .env
├── requirements.txt
└── run.py
```

## Setup

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add your Gemini API key in `.env`:
   ```bash
   GEMINI_API_KEY=your_real_key
   ```

## Run

```bash
flask --app run run --debug
```

Then open `http://127.0.0.1:5000/`.

## Test Gemini

Use this request to test Gemini before frontend integration:

```bash
curl -X POST http://127.0.0.1:5000/api/gemini \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Explain AI in one sentence"}'
```

The response is returned as JSON and also printed in the Flask terminal logs.
