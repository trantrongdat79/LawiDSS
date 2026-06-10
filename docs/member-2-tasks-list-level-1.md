# Member 2 Task List - Level 1

**Role:** AI Agent Engineer / Agentic Workflow Owner  
**Main responsibility:** Build the Agentic RAG workflow that connects legal retrieval, web evidence, LLM reasoning, and structured JSON output.

## 1. Role Summary

Member 2 owns the "brain" of the system. Member 1 provides the legal retrieval tool, Member 3 provides the UI and evaluation, and Member 2 connects everything into a working decision-support assistant.

The Agent must receive a user's labor-law situation, retrieve relevant legal basis, search for practical references, and return a structured advisory answer.

## 2. Main Tasks

### Task 1: Configure the LLM

**Purpose:** Prepare the model used by the Agent.

**Expected outcome:** A working LLM configuration using OpenAI, Groq, or another LlamaIndex-compatible provider.

### Task 2: Design the Agent Prompt

**Purpose:** Control how the Agent reasons and prevent hallucination.

**Expected outcome:** A system prompt that forces the Agent to cite retrieved law, avoid fake legal claims, separate legal basis from web examples, and return JSON.

### Task 3: Integrate Member 1's Legal Retrieval Tool

**Purpose:** Let the Agent retrieve official legal basis from the law database.

**Expected outcome:** The Agent can call `QueryEngineTool` and use its results as the only source for legal articles, clauses, and documents.

### Task 4: Build the Web Search Tool

**Purpose:** Find real-world labor-law cases or practical references.

**Expected outcome:** A DuckDuckGo Search Tool that returns article titles, URLs, and snippets for related cases.

### Task 5: Build the Web Scraper Tool

**Purpose:** Extract readable content from selected web search results.

**Expected outcome:** A scraper that returns clean article title, URL, and summary text, while handling failed or blocked pages safely.

### Task 6: Build the Agentic RAG Flow

**Purpose:** Coordinate all tools into one end-to-end workflow.

**Expected outcome:** The Agent can analyze the question, call the law tool, search the web, scrape references, and synthesize the final answer.

### Task 7: Return Structured JSON

**Purpose:** Give Member 3 a stable output format for Streamlit.

**Expected outcome:** Every final response follows this schema:

- `case_summary`
- `legal_issues`
- `legal_basis`
- `practical_references`
- `recommendations`
- `limitations`

### Task 8: Control Hallucination and Safety

**Purpose:** Make the system reliable enough for a legal decision-support demo.

**Expected outcome:** The Agent refuses or limits answers when legal evidence is missing, does not invent law, and clearly states that web sources are practical references only.

### Task 9: Support Evaluation and Demo

**Purpose:** Make the Agent testable and presentable.

**Expected outcome:** The Agent supports RAGAS evaluation, manual utility checks, latency measurement, and a clear final demo.

## 3. Basic Test Expectations

Member 2 should prepare tests for:

- valid JSON output
- legal retrieval integration
- mocked web search results
- readable, blocked, and invalid URLs for the scraper
- empty or weak legal retrieval results
- Agent behavior when web search fails
- end-to-end flow with mock law, search, and scraper tools

## 4. Final Deliverables

- Working Agentic RAG module.
- LLM configuration and system prompt.
- Integrated `QueryEngineTool`.
- DuckDuckGo Search Tool.
- Web Scraper Tool.
- Stable JSON output function/API for Streamlit.
- Test cases for tool behavior, JSON validity, hallucination control, and end-to-end flow.
- Demo-ready explanation of how the Agent calls tools and produces recommendations.
