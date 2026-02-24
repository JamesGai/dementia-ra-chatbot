# Dementia RA chatbot

This backend server is responsible for providing chatbot service to the [Dementia RA mobile application](https://github.com/JamesGai/dementia-ra.git). The implementation of this chatbot has two parts: LLM and knowledge base creation.

LLM is relatively eaiser as it only encompasses configuration and transmission to frontend. However, to build a knowledge base, we have to have a vector database ready with knowledge data being retrieved (from the database), transformed into JSON objects, and embedded by an embedding function.

There are also two types of knowledge, static knowledge and dynamic knowledge. Static knowledge is the built-in system message such as greetings, which is stored in data folder. Dynamic knowledge such as videos, courses, and services which changes rapidly as it is stored in the database.

To handle dynamic knowledge, we need to retrieve them from the database before embedding them.

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
python run.py
```

Then open `http://127.0.0.1:5000/`.
