# Member 2 Guide - Level 3

**Role:** AI Agent Engineer / Agentic Workflow Owner  
**Python version:** 3.14  
**Purpose:** Explain exactly how Member 2 should use the project structure and continue implementing the Agentic RAG workflow.

## 1. Big Picture

The project is split by responsibility:

- Member 1 owns legal retrieval in `src/retrieval/`.
- Member 2 owns Agentic RAG in `src/agent/`.
- Member 3 owns Streamlit and evaluation in `src/frontend/` and `src/evaluation/`.

You should treat `src/agent/` as your main workspace. Your module is the system's reasoning layer: it receives a question, asks the legal retrieval tool for legal basis, searches the web for practical references, scrapes useful pages, and returns JSON for the frontend.

## 2. Your Folder

```text
src/agent/
  __init__.py
  agent_workflow.py
  config.py
  llm_client.py

  prompts/
    system_prompt.md
    final_json_prompt.md

  schemas/
    __init__.py
    output_schema.py

  tools/
    __init__.py
    legal_retrieval_tool.py
    web_search_tool.py
    web_scraper_tool.py
```

## 3. File Responsibilities

### `config.py`

Loads environment variables and defaults.

Use this file when you need:

- OpenRouter base URL
- OpenRouter model
- LLM temperature
- max tokens
- web search limit
- scraper timeout

Do not hardcode these values in workflow files.

### `llm_client.py`

Contains the OpenRouter client.

This is the only file that should know:

- OpenRouter endpoint shape
- Bearer token authentication
- OpenRouter request payload
- OpenRouter response parsing

If the team later moves from OpenRouter to another provider, this file should absorb most of the change.

### `agent_workflow.py`

Contains the main function:

```python
answer_labor_law_question(question: str) -> dict
```

This is the function Member 3 should call from Streamlit.

### `schemas/output_schema.py`

Validates and normalizes the final JSON. This protects the frontend from malformed LLM output.

Keep the top-level fields stable:

- `case_summary`
- `legal_issues`
- `legal_basis`
- `practical_references`
- `recommendations`
- `limitations`

### `tools/legal_retrieval_tool.py`

Adapts Member 1's future `QueryEngineTool`.

This boundary matters. You should not depend on how Member 1 chunks documents, builds ChromaDB, or reranks results. You only need a query interface that returns legal results.

### `tools/web_search_tool.py`

Searches for practical references.

The current implementation is testable and has a basic DuckDuckGo HTML search fallback. In production, you may replace this with a more reliable API, but keep the same output shape.

### `tools/web_scraper_tool.py`

Fetches and extracts readable content from URLs.

It must handle:

- invalid URLs
- timeout
- empty pages
- blocked pages
- long pages

## 4. OpenRouter Setup

OpenRouter setup is your responsibility.

Create a local `.env` file from `.env.example`:

```env
OPENROUTER_API_KEY=your_real_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openrouter/free
LLM_TEMPERATURE=0.2
LLM_MAX_TOKENS=1200
WEB_SEARCH_MAX_RESULTS=5
SCRAPER_TIMEOUT_SECONDS=10
```

Rules:

- Never commit `.env`.
- Do not paste the API key into source code.
- Use `.env.example` to show teammates what variables are needed.
- Change models through `.env`, not code.

Smoke test:

```bash
python scripts/smoke_test_openrouter.py
```

If the smoke test fails, fix OpenRouter setup before debugging the Agent.

## 5. Agentic RAG Flow

The intended flow is:

1. User asks a labor-law question.
2. `answer_labor_law_question` validates the input.
3. The Agent identifies legal issue labels.
4. `LegalRetrievalAdapter` retrieves legal basis from Member 1's tool or mock data.
5. `DuckDuckGoSearchTool` searches for practical references.
6. `WebScraperTool` extracts readable text from selected URLs.
7. OpenRouter synthesizes the final JSON.
8. `output_schema.py` validates and normalizes the result.
9. The frontend receives a dictionary with stable fields.

## 6. Output Rules

The final response must be JSON-compatible. Do not return Markdown as the main output.

Legal basis rules:

- Must come only from Member 1's retrieval tool.
- Must not be invented by the LLM.
- Should include document name, article, effective status, excerpt, and source when available.

Practical reference rules:

- May come from web search and scraping.
- Must be labeled as practical examples only.
- Must not be treated as official law.

Recommendation rules:

- Give action options, not absolute commands.
- Order from lower-intensity to higher-intensity action.
- Include concrete steps.
- Include limitations.

## 7. Testing Guide

Run all normal tests:

```bash
python -m pytest tests
```

These tests use mocks and should not require API credits.

Run the OpenRouter smoke test only after `.env` is ready:

```bash
python scripts/smoke_test_openrouter.py
```

Key test files:

- `tests/unit/test_output_schema.py`
- `tests/unit/test_web_scraper_tool.py`
- `tests/unit/test_agent_workflow.py`

What each test protects:

- output schema tests protect the Streamlit contract
- scraper tests protect URL failure handling
- workflow tests protect end-to-end JSON behavior with mocks

## 8. How to Extend the Current Starter Code

Recommended next steps:

1. Ask Member 1 for the real `QueryEngineTool` interface.
2. Replace mock legal retrieval with the real tool.
3. Improve legal issue detection prompt.
4. Improve final synthesis prompt.
5. Add more tests for the six demo scenarios.
6. Add optional logging for tool calls and latency.
7. Coordinate with Member 3 to render every JSON field in Streamlit.

## 9. Common Mistakes to Avoid

- Do not put OpenRouter API keys in code.
- Do not edit Member 1's retrieval internals unless asked.
- Do not make the frontend parse free-form LLM text.
- Do not cite law from web articles.
- Do not trust LLM JSON without validation.
- Do not make tests depend on live OpenRouter calls.

## 10. Definition of Done for Member 2

Member 2's structure is being used correctly when:

- OpenRouter smoke test works with a real `.env`.
- Unit tests pass without an API key.
- `answer_labor_law_question` returns valid JSON.
- Legal basis comes from the retrieval adapter.
- Practical references come from search/scraper tools.
- The frontend can consume the response directly.
- The Agent handles missing law results and web failures gracefully.
