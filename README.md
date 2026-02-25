# Dementia RA chatbot

This backend server is responsible for providing chatbot service to the [Dementia RA mobile application](https://github.com/JamesGai/dementia-ra.git). The implementation of this chatbot has two parts: LLM and knowledge base creation.

LLM is relatively eaiser as it only encompasses configuration and transmission to frontend. However, to build a knowledge base, we have to have a vector database ready with knowledge data being retrieved (from the database), transformed into JSON objects, and embedded by an embedding function.

There are also two types of knowledge, static knowledge and dynamic knowledge. Static knowledge is the built-in system message such as greetings, which is stored in data folder. Dynamic knowledge such as videos, courses, and services which changes rapidly as it is stored in the database.

To handle dynamic knowledge, we need to retrieve them from the database before embedding them.

## Project structure

```text
.
├── app
│   ├── embeddings.py
│   ├── gemini.py
│   ├── static_knowledge_loader.py
│   └── dynamic_knowledge_service.py
├── data
│   ├── static_knowledge.json
├── scripts
│   ├── test_dynamic_knowledge_fetch.py
│   └── test_dynamic_knowledge_embeddings.py
├── .env
├── README.md
├── requirements.txt
├── chat_cli.py
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
## Vector Database (Chroma)

```bash
Static JSON - Static
Firestore (videos, course, services) - Dynamic
        ↓
Embedding (local or Gemini)
        ↓
Chroma vector database
```
One dependency in Chroma ```Pydantic``` is not compatible with the latest Python version ```python 3.14```. Therefore, we need to downgrade the python to a suitable version ```python 3.11```.
   - Install [Homebrew](https://brew.sh/) (Recommended)
      - Follow installation on official website
      - Verify installation
         - ```brew --version```
   - Install Python
      - ```brew install python@3.11```
      - Verify installation
         - ```python3.11 --version```
   - Create new virtual environment
      - Deactivate (if necessary)
         - ```deactivate```
      - Remove old virtrual environment
         - ```rm -rf .venv```
      - Create new one
         - ```python3.11 -m venv .venv```
      - Activate and verify python version
         - ```source .venv/bin/activate```
         - ```python --version```
      - [Official discussion](https://github.com/chroma-core/chroma/issues/5996) of this incompatibity

## Run

```bash
python run.py
```

Then open `http://127.0.0.1:5000/`.

## Chat in Terminal (No Frontend)

1. Start the Flask server:
   ```bash
   python run.py
   ```
2. In a second terminal (same virtual env), start the chat client:
   ```bash
   python chat_cli.py
   ```
