# Flask Starter

Minimal Flask project scaffold.

## Project structure

```text
.
├── app
│   ├── __init__.py
│   └── routes.py
├── .env.example
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
3. (Optional) load environment values:
   ```bash
   cp .env.example .env
   ```

## Run

```bash
flask --app run run --debug
```

Then open `http://127.0.0.1:5000/`.
