# Slacker AI Suite

This project provides a lightweight offline-first AI toolkit built with Python.
It includes a simple knowledge base with FAISS, integration with a local
Ollama LLM server, PDF utilities, and a FastAPI backend for interaction.

## Setup

Install dependencies and run the API server:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --reload
```

The API exposes endpoints for chatting with the model and managing the
knowledge base. Health check is available at `http://localhost:8000/health`.

## Tests

Run the automated tests with:

```bash
pytest
```
