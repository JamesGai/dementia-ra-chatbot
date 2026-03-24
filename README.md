# Dementia RA chatbot

This backend server is responsible for providing chatbot service to the [Dementia RA mobile application](https://github.com/JamesGai/dementia-ra.git). The implementation of this chatbot has two parts: LLM and knowledge base creation.

LLM is relatively eaiser as it only encompasses configuration and transmission to frontend. However, to build a knowledge base, we have to have a vector database ready with knowledge data being retrieved (from the database), transformed into JSON objects, and embedded by an embedding function.

There are also two types of knowledge, static knowledge and dynamic knowledge. Static knowledge is the built-in system message such as greetings, which is stored in data folder. Dynamic knowledge such as videos, courses, and services which changes rapidly as it is stored in the database.

To handle dynamic knowledge, we need to retrieve them from the database before embedding them.

## Project structure

![Chatbot Architecture](/public/Architecture.png)

```text
├── app
│   ├── embeddings.py
│   ├── gemini.py
│   ├── static_knowledge_loader.py
│   └── dynamic_knowledge_service.py - (video, course, service)
├── data
│   ├── static_knowledge.json
├── scripts
│   ├── ingest_to_chroma.py
│   ├── test_rag_chat.py
│   ├── test_vector_search.py
│   ├── test_dynamic_knowledge_fetch.py
│   └── test_dynamic_knowledge_embeddings.py
├── .env
├── README.md
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
4. Select embedding function in `.env`:
   ```bash
   EMBEDDING_PROVIDER=gemini
   ```
   ```bash
   EMBEDDING_PROVIDER=local
   ```

## Vector Database (Chroma Local or Cloud)

```bash
Static JSON - Static knowledge
Firestore (videos, course, services) - Dynamic knowledge
        ↓
Embedding (local or Gemini)
        ↓
Chroma vector database
```

### Python 3.11 setup

One dependency in Chroma `Pydantic` is not compatible with the latest Python version `python 3.14`. Therefore, we need to downgrade the python to a suitable version `python 3.11`.

- Install [Homebrew](https://brew.sh/) (Recommended)
  - Follow installation on official website
  - Verify installation
    - `brew --version`
- Install Python
  - `brew install python@3.11`
  - Verify installation
    - `python3.11 --version`
- Create new virtual environment
  - Deactivate (if necessary)
    - `deactivate`
  - Remove old virtrual environment
    - `rm -rf .venv`
  - Create new one
    - `python3.11 -m venv .venv`
  - Activate and verify python version
    - `source .venv/bin/activate`
    - `python --version`
  - [Official discussion](https://github.com/chroma-core/chroma/issues/5996) of this incompatibity

### Database setup

1. Transform static and dynamic knowledge into embeddings then load to Chroma Local or Cloud:
   ```bash
   python scripts/ingest_to_chroma_<local><cloud>.py
   ```

## App

- `<video><course><service>_service.py`:
  - Return all **video**/**course**/**service** knowledge as JSON objects ready for embedding
- `firestore_client.py`
  - Firebase configuration targets to dynamic knowledge retrieval
- `embeddings.py`
  - Transform data into embeddings using either local or cloud (Gemini) embedding function
- `gemini.py`
  - LLM (Gemini 2.5 Flash) configuration and inference
- `rag_service.py`
  - Full RAG pipeline, with retrieval function, prompt construction, and final answer generation implemented
  - This is where LLM needs to go through in order to generate context-relevant response
- `routes.py`
  - Raw and RAG-pipelined LLM endpoints
- `static_knowledge_loader.py`
  - Helper function that reads all built-in JSON data
- `vector_store_local.py`
  - Helpers for creating and accessing the project's local Chroma vector store
- `vector_store_cloud.py`
  - Helpers for creating and accessing the project's Chroma Cloud vector store

## Scripts

- Fetch and display transformed **video**/**course**/**service** knowledge as JSON objects:
  ```bash
  python scripts/test/test_<video><course><service>_fetch.py
  ```
- Generate and display embeddings of fetched **video**/**course**/**service** knowledge:
  ```bash
  python scripts/test/test_<video><course><service>_embeddings.py
  ```
- Transform static and dynamic knowledge into embeddings then load to local Chroma:
  ```bash
  python scripts/ingest_to_chroma_local.py
  ```
  Transform static and dynamic knowledge into embeddings then load to Chroma Cloud:
  ```bash
  python scripts/ingest_to_chroma_cloud.py
  ```
- Embed a query, run search in Chroma vector database, and print the top 3 matches:
  ```bash
  python scripts/test/test_vector_search.py
  ```
- Run a simple CLI loop to manually test RAG chat responses:
  ```bash
  python scripts/test/test_rag_chat.py
  ```

## Deployment

This chatbot service is hosted on Render

## Start Server

```bash
python run.py
```

Then open `http://127.0.0.1:5050/`.
