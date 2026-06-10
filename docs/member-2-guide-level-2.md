# Member 2 Guide - Level 2

**Role:** AI Agent Engineer / Agentic Workflow Owner  
**Python version:** 3.14  
**Main folder:** `src/agent/`

## 1. Your Responsibility

You are responsible for the Agentic RAG workflow. The system should receive a labor-law question, retrieve legal basis, search for practical references, scrape useful pages, and return structured JSON.

You do not build the legal database or the Streamlit UI. Instead:

- Member 1 gives you a future `QueryEngineTool`.
- Member 3 consumes your JSON output.
- You build the bridge between retrieval, LLM reasoning, web references, and final recommendations.

## 2. Folder Map

Use these folders:

```text
src/agent/
  agent_workflow.py
  config.py
  llm_client.py
  prompts/
  schemas/
  tools/
```

Important files:

- `config.py`: loads `.env` and runtime defaults
- `llm_client.py`: isolated OpenRouter client
- `agent_workflow.py`: main Agentic RAG flow
- `schemas/output_schema.py`: validates final JSON
- `tools/legal_retrieval_tool.py`: adapter for Member 1
- `tools/web_search_tool.py`: DuckDuckGo search interface
- `tools/web_scraper_tool.py`: readable web content extraction

## 3. OpenRouter Setup

OpenRouter setup is your responsibility because the Agent depends on LLM access.

Steps:

1. Create an OpenRouter account.
2. Create a project API key.
3. Copy `.env.example` to `.env`.
4. Add your real key to `.env`.
5. Run the smoke test.

Your `.env` should look like:

```env
OPENROUTER_API_KEY=your_real_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openrouter/free
LLM_TEMPERATURE=0.2
LLM_MAX_TOKENS=1200
WEB_SEARCH_MAX_RESULTS=5
SCRAPER_TIMEOUT_SECONDS=10
```

Do not commit `.env`.

## 4. Main Workflow

The main function is:

```python
answer_labor_law_question(question: str) -> dict
```

Expected flow:

1. Validate the user question.
2. Identify legal issues.
3. Retrieve legal basis through `LegalRetrievalAdapter`.
4. Build a practical-reference search query.
5. Search the web.
6. Scrape selected URLs.
7. Ask the LLM to synthesize final JSON.
8. Validate the JSON before returning.

## 5. Output Contract

Always return these fields:

- `case_summary`
- `legal_issues`
- `legal_basis`
- `practical_references`
- `recommendations`
- `limitations`

Member 3's frontend should never need to parse free-form text.

## 6. Testing Workflow

Normal tests do not require OpenRouter:

```bash
python -m pytest tests
```

OpenRouter smoke test requires a real key:

```bash
python scripts/smoke_test_openrouter.py
```

Test priorities:

- valid JSON output
- empty user question
- empty legal retrieval
- web search failure
- scraper invalid URL
- scraper readable HTML
- Agent end-to-end flow with mocks

## 7. How to Work With Other Members

With Member 1:

- Do not touch retrieval internals.
- Ask only for the `QueryEngineTool` interface and output shape.
- Keep using `LegalRetrievalAdapter` as the boundary.

With Member 3:

- Keep field names stable.
- Return JSON, not Markdown.
- Tell Member 3 when the schema changes.

## 8. Safety Rules

- Do not invent legal articles.
- Do not treat web articles as official law.
- If retrieval is empty, be cautious.
- Always include limitations.
- Recommendations should be options, not commands.
