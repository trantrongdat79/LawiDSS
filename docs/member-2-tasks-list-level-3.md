# Member 2 Task List - Level 3

**Role:** AI Agent Engineer / Agentic Workflow Owner  
**Audience:** A human engineer or AI agent that must implement Member 2's work without asking major follow-up questions.  
**Goal:** Build a reliable Agentic RAG module for a Vietnamese labor-law decision-support system.

## 1. Mission and Boundaries

Member 2 owns the Agentic Workflow. This is the reasoning and orchestration layer that turns retrieved legal documents and web references into a structured decision-support answer.

Member 2 must build the module that:

1. Receives a user's natural-language labor-law situation.
2. Identifies the main legal issues.
3. Calls Member 1's legal retrieval tool for official legal basis.
4. Searches the web for practical references.
5. Scrapes readable content from selected URLs.
6. Synthesizes the final answer.
7. Returns stable JSON for Member 3's Streamlit frontend and evaluation scripts.

Member 2 must not own:

- legal dataset cleaning and vector database construction, which belong to Member 1
- Streamlit UI design and RAGAS scoring scripts, which belong to Member 3
- official legal verification outside retrieved documents

Member 2 must still coordinate with Members 1 and 3 on interfaces, expected output, integration testing, and demo readiness.

## 2. End-to-End Target Flow

The final Agentic RAG flow should behave like this:

1. User submits a question, for example: "My company has not paid my salary for 2 months and asks me to sign a resignation letter. What should I do?"
2. Agent identifies legal issues such as unpaid salary, forced resignation, labor contract termination, evidence collection, and complaint options.
3. Agent calls Member 1's `QueryEngineTool`.
4. Legal retrieval returns relevant legal snippets with metadata.
5. Agent creates one or more web search queries for similar real-world situations.
6. Agent calls DuckDuckGo Search Tool.
7. Agent selects the most relevant 1-3 results.
8. Agent calls Web Scraper Tool for selected URLs.
9. Agent synthesizes legal basis, practical references, and action options.
10. Agent returns valid JSON using the required schema.

Expected outcome: the project has one callable Agentic RAG backend entrypoint that can be connected to Streamlit and evaluation scripts.

## 3. Required JSON Output Contract

Every final Agent response must use this schema exactly. Field names must not change.

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

Rules for this schema:

- `case_summary` must summarize the user's situation in 1-3 sentences.
- `legal_issues` must list the legal problems detected from the question.
- `legal_basis` must contain only law retrieved from Member 1's `QueryEngineTool`.
- `practical_references` must contain only web examples or related real-world references.
- `recommendations` must be action options, not absolute commands.
- `limitations` must always state that the system is only decision support and does not replace official legal advice.

## 4. Work Package A: LLM Configuration

### Objective

Configure the LLM used by the ReAct Agent and final synthesis step.

### Implementation tasks

- Choose a model provider that works with LlamaIndex, such as OpenAI, Groq, or another compatible chat model.
- Load API credentials from environment variables or local project configuration.
- Use a low temperature setting, preferably between `0` and `0.3`.
- Use a model capable of following structured-output instructions.
- Create a small smoke-test function that sends a simple prompt and returns the model response.
- Document required environment variables for teammates.

### Expected outcome

- The project can initialize the LLM without hardcoded secrets.
- The LLM can be reused by the Agent, final JSON synthesis, and tests.
- Missing configuration fails with a clear error message.

### Acceptance criteria

- A teammate can run the LLM smoke test after setting credentials.
- Model output is stable enough for structured JSON tasks.
- No API key is committed into the repository.

### Test cases

- **Valid configuration:** API key exists, model initializes, simple prompt returns response.
- **Missing key:** API key is absent, initialization returns a clear setup error.
- **Repeated call stability:** same simple prompt is called multiple times and response structure remains stable.

## 5. Work Package B: Prompt and Hallucination Control

### Objective

Design the Agent instructions so the system is careful, source-grounded, and useful for legal decision support.

### Required prompt rules

The system prompt must instruct the Agent to:

- always retrieve legal basis before making legal conclusions
- never invent legal articles, clauses, document names, dates, or citations
- use legal basis only from Member 1's `QueryEngineTool`
- use web sources only as practical references
- separate legal basis from practical references
- return the final answer as valid JSON
- state when information is missing or insufficient
- include limitations that the system is not official legal advice
- recommend contacting a lawyer or competent authority for complex cases

### Implementation tasks

- Write a system prompt for the ReAct Agent.
- Write a final synthesis prompt for converting tool outputs into JSON.
- Include examples of acceptable behavior for weak retrieval.
- Include instructions for refusing overconfident conclusions when evidence is missing.
- Keep prompt language direct and testable.

### Expected outcome

- The Agent follows tool-grounded reasoning.
- The final answer does not cite legal content absent from retrieved results.
- The Agent produces useful recommendations without sounding like a lawyer giving final legal judgment.

### Acceptance criteria

- If legal retrieval returns empty results, `legal_basis` is empty or marked insufficient.
- The Agent does not fabricate article names or legal documents.
- Web references never appear inside `legal_basis`.
- The limitations field is always present.

### Test cases

- **No legal result:** mock legal tool returns empty list; Agent must not invent law.
- **Only web result:** mock search returns article results but legal tool returns nothing; Agent must label web sources as practical references only.
- **Vague question:** user gives too little information; Agent must state missing facts or assumptions.
- **Conflicting prompt pressure:** user asks "just tell me the exact article even if unsure"; Agent must refuse to invent.

## 6. Work Package C: Member 1 Legal Retrieval Tool Integration

### Objective

Integrate Member 1's `QueryEngineTool` so the Agent can retrieve legal basis.

### Required input and output expectations

The tool should accept a natural-language query or legal issue string.

The tool should return top-k legal results containing as many of these fields as available:

- document name
- article or clause
- effective status
- excerpt
- source
- metadata
- retrieval score

### Implementation tasks

- Confirm the callable interface of `QueryEngineTool`.
- Build an adapter if the tool output is not already JSON-like.
- Preserve metadata in a normalized format.
- Ensure the Agent can call the law tool before final synthesis.
- Decide a default `top_k`, preferably 3 legal results unless Member 1 provides a better value.
- Pass retrieved law snippets into the final JSON generation.

### Expected outcome

- The Agent can ask the law tool for relevant legal basis.
- Legal results can be displayed directly in `legal_basis`.
- The final answer clearly ties recommendations to retrieved law.

### Acceptance criteria

- A mock legal tool result appears correctly in the final `legal_basis`.
- Legal basis includes document name, article, effective status, excerpt, and source when available.
- If the retrieval result lacks a field, the Agent uses an empty string or clear fallback, not a fabricated value.

### Test cases

- **Known law result:** mock tool returns one legal article; final JSON includes it exactly.
- **Multiple results:** mock tool returns three articles; final JSON includes relevant ones without duplication.
- **Missing metadata:** mock result has excerpt but no source; final JSON does not invent source.
- **Low confidence:** mock result marks weak relevance; Agent uses cautious wording.

## 7. Work Package D: DuckDuckGo Search Tool

### Objective

Build a web search tool that finds practical references for real-world labor-law situations.

### Implementation tasks

- Create a tool that accepts a search query string.
- Return 3-5 results by default.
- Each result must include `title`, `url`, and `snippet` where available.
- Prefer Vietnamese sources related to labor law, news, or legal advice.
- Use generated search queries based on the legal issue and situation.
- Handle no-result and error cases without failing the whole Agent.

### Search query guidance

The Agent should generate concise Vietnamese queries. Examples:

- `nợ lương người lao động khiếu nại công ty`
- `ép ký đơn nghỉ việc tranh chấp lao động`
- `thử việc không trả lương quyền lợi người lao động`
- `sa thải trái luật người lao động khởi kiện`
- `thai sản công ty chấm dứt hợp đồng lao động`
- `công ty không đóng bảo hiểm xã hội người lao động`

### Expected outcome

- The Agent can find practical references related to the user situation.
- Web search output is structured and ready for scraping.
- Search failure does not block the legal answer.

### Acceptance criteria

- Tool returns a list, even when empty.
- Each successful result has at least a URL.
- Search errors are represented as controlled failure messages.
- The Agent can continue with only legal basis if search fails.

### Test cases

- **Mock successful search:** returns three results with title, URL, snippet.
- **No results:** returns empty list and Agent still produces legal answer.
- **Search error:** returns controlled error and Agent states practical references are unavailable.
- **Irrelevant results:** Agent should avoid using obviously unrelated results in final references.

## 8. Work Package E: Web Scraper Tool

### Objective

Build a scraper that extracts readable content from URLs returned by web search.

### Implementation tasks

- Create a tool that accepts a URL.
- Fetch page content with timeout handling.
- Extract title and main readable text.
- Remove scripts, navigation, footer, ads, and repeated unrelated page text where practical.
- Limit extracted content before passing to the LLM.
- Return status as `success` or `failed`.
- Preserve the original URL.

### Recommended scraper output

```json
{
  "title": "Article title",
  "url": "https://example.com",
  "content_excerpt": "Cleaned article excerpt...",
  "status": "success"
}
```

Failure output:

```json
{
  "title": "",
  "url": "https://example.com",
  "content_excerpt": "",
  "status": "failed",
  "error": "Could not extract readable content"
}
```

### Expected outcome

- The Agent can read practical references from selected URLs.
- Scraped content is clean enough for summarization.
- Bad pages do not crash the Agent.

### Acceptance criteria

- Readable pages produce non-empty title or content excerpt.
- Invalid URLs return a failed status.
- Blocked or unreadable pages return a failed status.
- Long pages are truncated before LLM input.

### Test cases

- **Readable HTML:** mocked HTML contains article text; scraper extracts title and main content.
- **Invalid URL:** scraper returns failed status.
- **Timeout:** scraper returns failed status without blocking indefinitely.
- **Empty page:** scraper returns failed status or empty excerpt clearly.
- **Long page:** scraper truncates content to the configured limit.

## 9. Work Package F: Agentic RAG Orchestration

### Objective

Build the main Agent workflow that connects LLM reasoning, legal retrieval, web search, scraping, and final answer synthesis.

### Implementation tasks

- Create the main callable function, for example `answer_labor_law_question(question: str)`.
- Validate that the input question is non-empty.
- Ask the Agent to identify likely legal issues.
- Call `QueryEngineTool` to retrieve legal basis.
- Generate a practical-reference search query.
- Call DuckDuckGo Search Tool.
- Select 1-3 search results for scraping.
- Call Web Scraper Tool on selected URLs.
- Summarize scraped practical references.
- Generate final JSON response.
- Return JSON to Member 3's frontend.

### Required behavior

- The law tool should normally be called before final answer generation.
- The web search tool should usually be called for the Agentic RAG pipeline because the project compares it against traditional RAG.
- If web search fails, the Agent should still answer using retrieved legal basis.
- If legal retrieval fails, the Agent should not make firm legal conclusions.
- If both legal retrieval and web search fail, the Agent should return a cautious response with limitations.

### Expected outcome

- The project has a full Agentic RAG pipeline ready for Streamlit integration.
- The workflow can be tested with mocked tools.
- Tool failures degrade gracefully.

### Acceptance criteria

- A valid user question returns valid JSON.
- The final JSON includes all required fields.
- Tool call failures do not crash the main function.
- Final recommendations are grounded in retrieved legal basis when available.

### Test cases

- **Happy path:** law tool, search tool, and scraper all return data; output includes all major sections.
- **Search unavailable:** law tool works, search fails; output includes legal basis and states practical references unavailable.
- **Scraper partly fails:** one URL works and one fails; output uses the successful reference only.
- **Law retrieval empty:** output avoids fake law and gives cautious recommendations.
- **Empty input:** function returns validation error or controlled response.

## 10. Work Package G: Final JSON Validation and Repair

### Objective

Ensure every response sent to Streamlit is valid and schema-compatible.

### Implementation tasks

- Parse the LLM final answer as JSON before returning.
- Check that required fields exist.
- Ensure list fields are arrays, even when empty.
- Ensure each `legal_basis` item has the expected keys.
- Ensure each `practical_references` item has title, URL, and summary.
- Ensure each `recommendations` item has option, when_to_use, and suggested_steps.
- Add a fallback response if JSON parsing fails.

### Expected outcome

- Member 3 can display the response without fragile parsing.
- Evaluation scripts can consume the same output.
- Malformed LLM output does not break the UI.

### Acceptance criteria

- Every successful call returns parseable JSON.
- All required top-level fields are present.
- Array fields remain arrays.
- Fallback output is safe and includes limitations.

### Test cases

- **Valid JSON:** parsed successfully and returned unchanged.
- **Missing field:** validator adds default empty value or fails gracefully.
- **Wrong type:** validator converts or rejects safely.
- **Malformed JSON:** fallback response is returned.

## 11. Work Package H: Recommendation Design

### Objective

Produce useful decision-support recommendations, not just legal explanations.

### Implementation tasks

- Convert retrieved law and practical references into action options.
- Order recommendations from lower-intensity to higher-intensity action.
- Include practical steps such as collecting evidence, sending written requests, contacting HR, filing a complaint, or seeking legal help.
- Avoid guaranteeing outcomes.
- Avoid telling the user to sue immediately unless the situation and legal basis support escalation.

### Recommended action ladder

1. Clarify facts and collect evidence.
2. Communicate or negotiate in writing.
3. Ask HR or employer for written explanation.
4. Contact labor authority or social insurance authority where relevant.
5. Consider mediation, complaint, or lawsuit for serious cases.
6. Contact a lawyer or competent authority for complex disputes.

### Expected outcome

- The final response helps the user choose a next step.
- Recommendations are specific enough for a demo.
- The answer clearly reflects a Decision Support System, not a generic chatbot.

### Acceptance criteria

- Each recommendation has `option`, `when_to_use`, and `suggested_steps`.
- Recommendations are connected to the user's situation.
- Recommendations remain cautious and non-final.
- Limitations are always included.

### Test cases

- **Unpaid salary:** recommendations include evidence collection, written salary request, and possible complaint.
- **Forced resignation:** recommendations include not signing unclear documents, preserving evidence, and requesting written explanation.
- **Probation issue:** recommendations include checking probation agreement and salary/payment terms.
- **Wrongful dismissal:** recommendations include collecting termination decision and checking legal basis.
- **Maternity issue:** recommendations include checking protection rules and social insurance/maternity benefits.
- **Social insurance issue:** recommendations include checking contribution records and contacting social insurance authority.

## 12. Work Package I: Evaluation Support

### Objective

Make Member 2's module easy to evaluate with RAGAS and manual project metrics.

### Implementation tasks

- Expose the Agent output in a way Member 3 can call repeatedly.
- Preserve source snippets used in the answer where practical.
- Return or log tool-call traces for debugging and demo.
- Measure latency for each major phase if possible: legal retrieval, search, scraping, final synthesis.
- Support a fixed test set of 30-50 questions from Member 3.

### Metrics supported

- Faithfulness: final answer should be grounded in retrieved law and scraped references.
- Answer Relevance: answer should address the user's situation.
- Citation quality: legal basis and URLs should be inspectable.
- Latency: Agentic RAG should be measured and compared with traditional RAG.
- User utility: recommendations should be clear and actionable.

### Expected outcome

- Member 3 can run evaluation without modifying Member 2's code heavily.
- The team can compare traditional RAG and Agentic RAG.
- The final report can explain strengths and tradeoffs.

### Acceptance criteria

- Agent can run on a batch of test questions.
- Each result contains the required JSON fields.
- Tool failures are visible enough to debug.
- Latency can be measured externally or internally.

### Test cases

- Run 5 representative scenarios manually before full evaluation.
- Run at least one batch test using mocked tools.
- Confirm output is compatible with RAGAS input preparation.
- Confirm source URLs are available for practical references.

## 13. Work Package J: Integration with Member 3 Frontend

### Objective

Provide a clean backend response that Streamlit can display.

### Implementation tasks

- Confirm the frontend expects the JSON schema from this document.
- Provide a single function/API endpoint that accepts `question` and returns JSON.
- Return errors in a controlled format when something fails.
- Keep field names stable.
- Avoid mixing raw LLM text with JSON unless explicitly requested by Member 3.

### Expected outcome

- Streamlit can show the Agent response in sections:
  - case summary
  - legal issues
  - legal basis
  - practical references
  - recommendations
  - limitations

### Acceptance criteria

- Member 3 can call the backend with a user question.
- Frontend does not need to parse free-form text.
- Failed responses still display a useful message.

### Test cases

- Frontend calls backend with a normal question and displays all sections.
- Frontend calls backend when web search fails and still displays legal basis.
- Frontend calls backend when Agent returns fallback JSON.

## 14. Work Package K: Demo Readiness

### Objective

Prepare Member 2's part for final project demonstration.

### Implementation tasks

- Prepare 2-3 demo questions that clearly show Agentic RAG value.
- Show that the Agent calls the legal retrieval tool.
- Show that the Agent calls web search and scraper.
- Show final JSON or UI sections.
- Prepare a short explanation of how Agentic RAG differs from traditional RAG.
- Prepare fallback demo behavior in case internet access or web search fails.

### Recommended demo questions

- "My company has not paid my salary for 2 months and asks me to sign a resignation letter. What should I do?"
- "I am pregnant and my company wants to terminate my labor contract. Is this allowed?"
- "My company does not pay social insurance for me. What options do I have?"

### Expected outcome

- The team can demo the reasoning flow clearly.
- The Agentic RAG system shows practical references and recommendations beyond baseline RAG.

### Acceptance criteria

- Demo questions produce stable JSON.
- Tool calls can be explained.
- At least one demo can run with mocked web results if live search fails.

## 15. Representative Test Scenario Set

Use these scenarios for manual testing before full evaluation.

### Scenario 1: Unpaid salary

Input:

> My company has not paid my salary for 2 months. What can I do?

Expected behavior:

- Detect unpaid salary issue.
- Retrieve relevant wage/payment legal basis.
- Search for practical unpaid-salary references.
- Recommend evidence collection, written request, complaint, and legal help if needed.

### Scenario 2: Forced resignation

Input:

> My employer asks me to sign a resignation letter even though I do not want to quit.

Expected behavior:

- Detect forced resignation and termination-risk issues.
- Retrieve legal basis related to termination or resignation where available.
- Recommend not signing unclear documents and preserving evidence.

### Scenario 3: Probation

Input:

> I worked during probation but the company does not want to pay me.

Expected behavior:

- Detect probation salary/payment issue.
- Retrieve relevant probation or wage legal basis.
- Recommend checking written agreement and requesting payment in writing.

### Scenario 4: Dismissal

Input:

> The company dismissed me without prior notice and without explaining the reason.

Expected behavior:

- Detect possible wrongful dismissal or unilateral termination issue.
- Retrieve relevant legal basis.
- Recommend collecting termination documents and asking for written reasons.

### Scenario 5: Maternity

Input:

> I am pregnant and my company wants to end my labor contract.

Expected behavior:

- Detect maternity protection and termination issue.
- Retrieve relevant legal basis.
- Recommend checking contract status, preserving communication, and contacting authority or lawyer.

### Scenario 6: Social insurance

Input:

> My company has not paid social insurance for me even though it deducts money from my salary.

Expected behavior:

- Detect social insurance contribution issue.
- Retrieve relevant legal basis if available.
- Recommend checking contribution records and contacting social insurance authority.

## 16. Weekly Implementation Checklist

### Week 1: Setup and Prototype

- Set up LlamaIndex and LLM provider.
- Create initial Agent prototype using mock legal data.
- Draft system prompt.
- Draft final JSON synthesis prompt.
- Confirm JSON schema with Member 3.

Expected outcome: mock Agent can receive a question and return JSON-like output.

### Week 2: Web Tools

- Build DuckDuckGo Search Tool.
- Build Web Scraper Tool.
- Test search and scraper independently.
- Add graceful failure behavior.

Expected outcome: web tools work independently and return structured data.

### Week 3: Full Agent Integration

- Integrate Member 1's `QueryEngineTool`.
- Connect legal retrieval, web search, scraper, and final synthesis.
- Return valid JSON.
- Test end-to-end with representative scenarios.

Expected outcome: working Agentic RAG backend.

### Week 4: Evaluation and Tuning

- Tune prompt based on evaluation errors.
- Improve hallucination control.
- Improve JSON validation.
- Improve latency where possible.
- Fix cases where Agent misuses web references as law.

Expected outcome: stable Agent ready for comparison against traditional RAG.

### Week 5: Packaging and Demo

- Support final Streamlit integration.
- Prepare demo questions.
- Prepare explanation of tool calls.
- Prepare fallback behavior for web failure.
- Help finalize report and slides for Agentic RAG section.

Expected outcome: demo-ready Agentic RAG module.

## 17. Final Deliverables

Member 2 is done when the following deliverables exist:

- LLM configuration and smoke test.
- ReAct Agent prompt and final synthesis prompt.
- Integration with Member 1's `QueryEngineTool`.
- DuckDuckGo Search Tool.
- Web Scraper Tool.
- Main Agentic RAG function/API.
- JSON validation and fallback behavior.
- Tool-level tests for law tool adapter, search, and scraper.
- End-to-end tests with mocked tools.
- Manual scenario tests for unpaid salary, forced resignation, probation, dismissal, maternity, and social insurance.
- Demo notes explaining how Agentic RAG supports decision-making.

## 18. Definition of Done

The Member 2 work is complete when:

- A user question can go through the full Agentic RAG flow.
- The law tool is used for legal basis.
- Web search and scraper are used for practical references.
- The final answer is valid JSON.
- The answer includes recommendations and limitations.
- The Agent does not invent legal citations.
- The system handles missing law results and web failures gracefully.
- Member 3 can consume the output in Streamlit.
- The module can be evaluated on the project test set.
- The demo can show the difference between traditional RAG and Agentic RAG.
