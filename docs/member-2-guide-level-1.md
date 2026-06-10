# Member 2 Guide - Level 1

**Role:** AI Agent Engineer / Agentic Workflow Owner  
**Main folder:** `src/agent/`

## 1. What You Own

You own the Agentic RAG workflow. Your job is to connect:

- Member 1's legal retrieval tool
- OpenRouter LLM calls
- web search
- web scraping
- final JSON output for Member 3's Streamlit UI

## 2. Folders You Should Use

- `src/agent/`: your main code
- `src/agent/tools/`: legal retrieval adapter, web search, web scraper
- `src/agent/schemas/`: final output validation
- `src/agent/prompts/`: Agent and JSON prompts
- `tests/unit/`: your unit tests
- `scripts/smoke_test_openrouter.py`: checks OpenRouter access

## 3. Folders You Should Not Own

- `src/retrieval/`: Member 1 owns legal data and retrieval
- `src/frontend/`: Member 3 owns Streamlit UI
- `src/evaluation/`: Member 3 owns evaluation scripts

Use those folders only through agreed interfaces.

## 4. OpenRouter Setup

Create a local `.env` file from `.env.example`:

```env
OPENROUTER_API_KEY=your_real_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openrouter/free
LLM_TEMPERATURE=0.2
```

Never commit `.env`.

## 5. Main Function

The main function is:

```python
answer_labor_law_question(question: str) -> dict
```

It lives in:

```text
src/agent/agent_workflow.py
```

Member 3 should call this function from Streamlit.

## 6. How to Test

Run:

```bash
python -m pytest tests
```

Run the OpenRouter smoke test only after adding your real API key:

```bash
python scripts/smoke_test_openrouter.py
```

## 7. Golden Rule

Legal basis must come only from Member 1's retrieval tool. Web sources are practical references only, not official law.
