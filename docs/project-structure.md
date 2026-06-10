# Project Structure and Setup Guide

This document explains how the project directory should be organized and where each member's work should live. The goal is to keep the project easy to understand, easy to run with Docker Compose, and easy for another teammate or AI agent to continue.

## 1. Recommended Directory Structure

```text
Project/
  docs/
    proposal.md
    project-plan.md
    project-structure.md
    member-2-tasks-list-level-1.md
    member-2-tasks-list-level-2.md
    member-2-tasks-list-level-3.md

  data/
    raw/
    processed/
    indexes/

  src/
    common/
    retrieval/
    agent/
    frontend/
    evaluation/

  tests/
    unit/
    integration/
    fixtures/

  scripts/
  configs/
  docker/

  docker-compose.yml
  .env.example
  README.md
```

## 2. Directory Responsibilities

### `docs/`

Stores project documentation, task lists, architecture notes, and report drafts.

Expected content:

- proposal
- project plan
- project structure guide
- member task lists
- demo notes
- evaluation explanation

### `data/`

Stores data used by the system.

Recommended subfolders:

- `data/raw/`: original downloaded or exported legal datasets
- `data/processed/`: cleaned and chunked legal documents
- `data/indexes/`: vector database files such as ChromaDB indexes

Important: large data and generated indexes should usually be ignored by Git.

### `src/common/`

Stores shared utilities used across multiple modules.

Possible content:

- config loading
- logging setup
- shared constants
- common error types
- helper functions

### `src/retrieval/`

Owned mainly by Member 1.

Purpose:

- load legal documents
- clean HTML
- chunk by legal structure
- build vector database
- implement hybrid retrieval
- expose `QueryEngineTool` for Member 2

### `src/agent/`

Owned mainly by Member 2.

Purpose:

- configure the LLM provider
- call OpenRouter
- define Agent prompts
- integrate Member 1's `QueryEngineTool`
- build DuckDuckGo Search Tool
- build Web Scraper Tool
- run the Agentic RAG workflow
- return stable JSON for Streamlit

Recommended internal structure:

```text
src/agent/
  __init__.py
  agent_workflow.py
  llm_client.py
  config.py

  prompts/
    system_prompt.md
    final_json_prompt.md

  tools/
    legal_retrieval_tool.py
    web_search_tool.py
    web_scraper_tool.py

  schemas/
    output_schema.py
```

### `src/frontend/`

Owned mainly by Member 3.

Purpose:

- Streamlit UI
- receive user question
- call backend/Agent function
- display case summary, legal basis, practical references, recommendations, and limitations

### `src/evaluation/`

Owned mainly by Member 3, with support from Members 1 and 2.

Purpose:

- ground truth questions
- retrieval metrics such as Hit Rate and MRR
- RAGAS evaluation
- latency measurement
- comparison between traditional RAG and Agentic RAG

### `tests/`

Stores automated tests.

Recommended subfolders:

- `tests/unit/`: test individual tools and helpers
- `tests/integration/`: test multiple modules together
- `tests/fixtures/`: mock legal results, mock search results, mock HTML pages

### `scripts/`

Stores command-line scripts for repeatable project actions.

Examples:

- build vector index
- run evaluation
- run demo data preparation
- smoke-test OpenRouter

### `configs/`

Stores non-secret configuration files.

Examples:

- model defaults
- retrieval settings
- scraper settings
- evaluation settings

Secrets must not be stored here.

## 3. OpenRouter Setup Responsibility

OpenRouter setup should be treated as a separate setup phase and should be your responsibility. This is important because Member 2's Agent depends on LLM access, and OpenRouter credentials must be configured safely before the Agentic RAG workflow can run.

## 4. OpenRouter Setup Tasks

### Task 1: Create an OpenRouter Account

Create an account at OpenRouter and prepare API access.

Expected outcome:

- You have an OpenRouter account.
- You can access the API key page.
- You understand the free-model request limits and whether your team needs a small credit top-up for final demo reliability.

### Task 2: Create an API Key

Create one API key for this project.

Expected outcome:

- One project-specific OpenRouter API key exists.
- The key is not shared publicly.
- The key is not committed to Git.

Recommended practice:

- Name the key clearly, for example `dss-labor-law-project`.
- Set a credit limit if OpenRouter allows it for the key.
- Rotate/delete the key immediately if it is accidentally exposed.

### Task 3: Add Environment Variables

Create a local `.env` file from `.env.example`.

`.env.example` should contain:

```env
OPENROUTER_API_KEY=
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openrouter/free
LLM_TEMPERATURE=0.2
```

Your local `.env` should contain the real API key:

```env
OPENROUTER_API_KEY=your_real_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openrouter/free
LLM_TEMPERATURE=0.2
```

Expected outcome:

- `.env.example` is committed.
- `.env` is not committed.
- Other members know which variables they need to set.

### Task 4: Add Git Ignore Rules for Secrets

Make sure secret files are ignored by Git.

Recommended `.gitignore` entries:

```gitignore
.env
.env.*
!.env.example
```

Expected outcome:

- Real API keys stay local.
- The repository still contains `.env.example` as a safe template.

### Task 5: Create the LLM Client Location

The OpenRouter client should live in:

```text
src/agent/llm_client.py
```

This file should be the only place that knows the OpenRouter API details.

Expected outcome:

- Other Agent files call a simple local function or class.
- The project can later switch from OpenRouter to another provider without rewriting the whole Agent.

Recommended responsibility split:

- You: OpenRouter account, API key, `.env.example`, Docker/env setup, smoke test.
- Member 2: use `llm_client.py` inside Agentic RAG.

### Task 6: Add an OpenRouter Smoke Test

Create a simple smoke test script later, preferably in:

```text
scripts/smoke_test_openrouter.py
```

The smoke test should:

- load `OPENROUTER_API_KEY`
- call the configured model
- ask for a tiny response
- print whether the call succeeded
- avoid using many tokens

Expected outcome:

- Before building the full Agent, the team can confirm LLM access works.
- OpenRouter errors are caught early.

### Task 7: Choose a Default Model Strategy

Start with:

```env
OPENROUTER_MODEL=openrouter/free
```

This keeps the project subscription-free while testing.

For final demo, prepare a fallback option:

```env
OPENROUTER_MODEL=some-specific-model-slug
```

Expected outcome:

- Development can use a free model.
- Demo can switch to a more reliable model if needed.
- Model choice is changed through `.env`, not by editing code.

## 5. Docker Compose Recommendation

Use Docker Compose to make the project easier to run, but do not create too many services.

Recommended services:

```text
app        shared Python backend code
streamlit  frontend UI
chroma     optional vector database service, if not using local persisted Chroma files
```

Recommended volume behavior:

- mount project source code into the container during development
- mount `data/indexes/` for vector database persistence
- pass OpenRouter variables through `.env`

Important:

- Do not put API keys directly inside `docker-compose.yml`.
- Use `.env` for local secret values.
- Keep `.env.example` as the committed template.

## 6. Recommended Implementation Order

1. Create the project directories.
2. Add `.gitignore` and `.env.example`.
3. Set up OpenRouter account and API key.
4. Add OpenRouter environment variables locally.
5. Create `src/agent/llm_client.py`.
6. Create `scripts/smoke_test_openrouter.py`.
7. Confirm the smoke test works.
8. Let Member 2 build the Agentic RAG workflow on top of the working LLM client.
9. Let Member 1 integrate retrieval through `QueryEngineTool`.
10. Let Member 3 connect Streamlit and evaluation.

## 7. Final Advice

Use directories to separate responsibilities, but keep the codebase as one project. This is easier than creating many independent services.

OpenRouter should be isolated behind `src/agent/llm_client.py`. The rest of the project should not depend directly on OpenRouter-specific details. This gives the team flexibility: if OpenRouter free models are too limited, you can switch to another model provider later by changing configuration and the LLM client only.
