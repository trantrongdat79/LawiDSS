# Labor Law Decision Support System

This project is a Decision Support System for Vietnamese labor-law situations. It compares a traditional legal RAG pipeline with an Agentic RAG pipeline that combines legal retrieval, web references, and structured recommendations.

## Python Version

Use Python 3.14 for development and Docker.

## Main Areas

- `src/retrieval/`: Member 1, legal data and retrieval.
- `src/agent/`: Member 2, OpenRouter LLM setup and Agentic RAG workflow.
- `src/frontend/`: Member 3, Streamlit UI.
- `src/evaluation/`: Member 3, evaluation scripts and metrics.

## Setup

1. Create a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill in `OPENROUTER_API_KEY`.

4. Run tests:

```bash
python -m pytest tests
```

5. Run the OpenRouter smoke test only after adding a real API key:

```bash
python scripts/smoke_test_openrouter.py
```

## Docker Compose

```bash
docker compose up --build
```

The current Docker setup is a development scaffold. Member 3 can later connect the Streamlit UI to the Agent workflow.
