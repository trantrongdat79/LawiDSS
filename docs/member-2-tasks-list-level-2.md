# Member 2 Task List - Level 2

**Role:** AI Agent Engineer / Agentic Workflow Owner  
**Goal:** Build the Agentic RAG module that combines legal retrieval, web search, web scraping, LLM reasoning, JSON output, and safety controls.

## 1. Responsibility Overview

Member 2 is responsible for the Agentic Workflow. This means building the part of the system that receives a natural-language labor-law question and decides how to use available tools to produce a structured decision-support answer.

Member 2 does not own the legal dataset or the Streamlit UI, but must integrate with both:

- Member 1 provides `QueryEngineTool`, which retrieves official legal basis.
- Member 3 consumes Member 2's JSON output in Streamlit and evaluates answer quality.

## 2. Core Workflow to Build

The Agentic RAG flow should work as follows:

1. Receive the user's labor-law situation.
2. Identify the main legal issues.
3. Call Member 1's `QueryEngineTool` to retrieve legal basis.
4. Generate a search query for practical references.
5. Call DuckDuckGo Search Tool.
6. Scrape the most relevant URLs.
7. Synthesize a structured advisory response.
8. Return valid JSON to the frontend.

Expected outcome: one callable backend function or API that takes a user question and returns a complete JSON response.

## 3. Task Group A: LLM Configuration

### Tasks

- Choose an LLM provider supported by the project stack, such as OpenAI, Groq, or another LlamaIndex-compatible model.
- Configure API key loading through environment variables or local configuration.
- Set model parameters for stable legal-domain output.
- Use a low temperature setting so answers are conservative and consistent.

### Expected outcome

- The Agent can call the configured LLM successfully.
- LLM settings are documented well enough for teammates to reproduce.
- Model output is stable enough for JSON generation and evaluation.

### Basic tests

- Run a simple prompt and confirm the model returns a response.
- Run the same legal-style input multiple times and check that the structure is stable.
- Confirm missing API keys produce a clear setup error rather than a confusing crash.

## 4. Task Group B: System Prompt and Safety Rules

### Tasks

- Write the main system prompt for the ReAct Agent.
- Instruct the Agent to always retrieve legal basis before giving legal conclusions.
- Instruct the Agent that legal basis must come only from `QueryEngineTool`.
- Instruct the Agent that web articles are practical references only, not official law.
- Require the Agent to return structured JSON.
- Require the Agent to say when information is insufficient.
- Add a standard limitation that the system is for decision support, not official legal advice.

### Expected outcome

- The Agent behaves like a careful legal decision-support assistant.
- It does not invent article numbers, legal documents, or fake citations.
- It separates legal basis, practical references, and recommendations.

### Basic tests

- Ask a question where the law tool returns no results and confirm the Agent does not invent law.
- Ask a question with a web article but no legal basis and confirm the article is not treated as official law.
- Ask a broad or vague question and confirm the Agent states assumptions or missing information.

## 5. Task Group C: Legal Retrieval Tool Integration

### Tasks

- Receive `QueryEngineTool` from Member 1.
- Confirm its input format, output format, and top-k behavior.
- Wrap or adapt the tool if needed so the Agent can call it consistently.
- Preserve important metadata from legal retrieval results.
- Pass legal excerpts and metadata to the final synthesis step.

### Expected outcome

- The Agent can call the legal retrieval tool during reasoning.
- Final JSON includes legal basis with document name, article, effective status, excerpt, and source when available.
- Legal claims in the final answer are grounded in retrieved legal content.

### Basic tests

- Use a mock `QueryEngineTool` returning known legal snippets.
- Confirm those snippets appear in `legal_basis`.
- Confirm the Agent does not cite legal documents that were not returned by the tool.

## 6. Task Group D: DuckDuckGo Search Tool

### Tasks

- Build a search tool that accepts a generated search query.
- Return a small list of practical references, preferably 3-5 results.
- Include title, URL, and snippet for each result.
- Prefer Vietnamese labor-law, news, or legal-advice sources where possible.
- Handle no-result and search-error cases safely.

### Expected outcome

- The Agent can search for real-world cases related to the user's situation.
- Search results are structured and ready for scraping.
- Failed search does not break the whole Agent flow.

### Basic tests

- Unit-test with mocked search results.
- Test no-result behavior.
- Test search-error behavior.
- Confirm returned results contain title, URL, and snippet.

## 7. Task Group E: Web Scraper Tool

### Tasks

- Build a scraper that accepts a URL.
- Extract title and readable main text.
- Remove navigation, scripts, ads, and unrelated page content as much as practical.
- Limit the extracted text length before sending it to the LLM.
- Return a safe failure object when the page cannot be read.

### Expected outcome

- The Agent can read practical references from selected URLs.
- Scraped content is short enough to fit into the prompt.
- Failed or blocked pages are skipped gracefully.

### Basic tests

- Test with a readable URL using mocked HTML.
- Test with invalid URLs.
- Test with blocked or empty content.
- Confirm output includes URL, title, content excerpt, and status.

## 8. Task Group F: Structured JSON Output

### Required schema

```json
{
  "case_summary": "Tóm tắt ngắn gọn tình huống người dùng",
  "legal_issues": [
    "Vấn đề pháp lý 1",
    "Vấn đề pháp lý 2"
  ],
  "legal_basis": [
    {
      "document_name": "Tên văn bản",
      "article": "Điều/Khoản",
      "effective_status": "Còn hiệu lực",
      "excerpt": "Trích đoạn liên quan",
      "source": "Nguồn văn bản nếu có"
    }
  ],
  "practical_references": [
    {
      "title": "Tiêu đề bài viết",
      "url": "https://example.com",
      "summary": "Tóm tắt tình huống thực tế"
    }
  ],
  "recommendations": [
    {
      "option": "Thương lượng với công ty",
      "when_to_use": "Khi tranh chấp còn có thể giải quyết nội bộ",
      "suggested_steps": [
        "Chuẩn bị hợp đồng, bảng lương, email, tin nhắn liên quan",
        "Gửi yêu cầu bằng văn bản"
      ]
    }
  ],
  "limitations": "Thông tin chỉ mang tính tham khảo, không thay thế tư vấn pháp lý chính thức."
}
```

### Tasks

- Force the final answer into the required JSON schema.
- Validate JSON before returning it to Member 3.
- Add fallback handling for malformed LLM output.
- Keep field names stable.

### Expected outcome

- Streamlit can display Agent results without custom parsing.
- Evaluation scripts can read the same output consistently.

### Basic tests

- Test that every response parses as valid JSON.
- Test that all required fields exist.
- Test that array fields are arrays even when empty.
- Test malformed LLM output recovery if a repair step is implemented.

## 9. Task Group G: Recommendation Logic

### Tasks

- Convert legal basis and practical references into decision-support recommendations.
- Present recommendations as options, not commands.
- Order options from low-intensity to high-intensity action.
- Include when each option is suitable.
- Include concrete suggested steps where possible.

### Expected outcome

- The final answer helps the user decide what to do next.
- The system feels like a DSS, not just a Q&A chatbot.

### Basic tests

- Ask an unpaid-salary question and confirm recommendations include evidence collection and written request.
- Ask a forced-resignation question and confirm recommendations mention preserving proof and avoiding unclear signatures.
- Confirm the Agent includes a limitation/disclaimer.

## 10. Task Group H: Evaluation and Demo Support

### Tasks

- Make the Agent callable by evaluation scripts.
- Log or return enough information to inspect tool calls during demo.
- Support RAGAS evaluation for Faithfulness and Answer Relevance.
- Support manual utility checks for recommendation quality.
- Measure latency for Agentic RAG.

### Expected outcome

- Member 3 can evaluate the Agent.
- The team can compare traditional RAG and Agentic RAG.
- The demo can clearly show why the Agentic workflow adds value.

### Basic tests

- Run the Agent on 5-6 representative labor-law scenarios.
- Confirm each response has legal basis, practical references, recommendations, and limitations.
- Confirm the Agent handles web search failure without losing legal answer quality.

## 11. Weekly Alignment

### Week 1

- Set up LlamaIndex and LLM.
- Build a prototype Agent using mock legal data.
- Draft system prompt and JSON output format.

### Week 2

- Complete DuckDuckGo Search Tool.
- Complete Web Scraper Tool.
- Test tools independently.

### Week 3

- Integrate Member 1's `QueryEngineTool`.
- Build end-to-end Agentic RAG flow.
- Connect backend output to Member 3's Streamlit expectations.

### Week 4

- Tune prompts.
- Reduce hallucination.
- Improve JSON reliability.
- Fix issues found during RAGAS and manual evaluation.

### Week 5

- Prepare demo behavior.
- Help debug final integration.
- Prepare explanation of Agent reasoning and tool calls.

## 12. Final Deliverables

- LLM setup and configuration.
- System prompt and hallucination-control rules.
- Integrated legal retrieval tool.
- DuckDuckGo Search Tool.
- Web Scraper Tool.
- Agentic RAG module.
- Stable JSON response function/API.
- Tool-level and end-to-end tests.
- Demo notes showing how the Agent supports decision-making.
