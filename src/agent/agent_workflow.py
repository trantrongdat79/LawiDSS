"""Main Agentic RAG workflow owned by Member 2."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from src.agent.config import load_config
from src.agent.llm_client import LLMClientError, OpenRouterClient
from src.agent.schemas.output_schema import (
    fallback_response,
    normalize_agent_response,
)
from src.agent.tools.legal_retrieval_tool import LegalRetrievalAdapter
from src.agent.tools.web_scraper_tool import WebScraperTool
from src.agent.tools.web_search_tool import (
    DuckDuckGoSearchTool,
    build_practical_search_query,
)


DEFAULT_LIMITATION = (
    "This system is for decision support only and does not replace official legal "
    "advice from a lawyer or competent authority."
)


@dataclass
class AgentDependencies:
    """Injectable dependencies for tests and integration."""

    llm_client: Any | None = None
    legal_tool: LegalRetrievalAdapter | None = None
    search_tool: DuckDuckGoSearchTool | None = None
    scraper_tool: WebScraperTool | None = None


def answer_labor_law_question(
    question: str,
    dependencies: AgentDependencies | None = None,
) -> dict[str, Any]:
    """Answer a labor-law question with Agentic RAG and return frontend JSON."""

    question = (question or "").strip()
    if not question:
        return fallback_response("", "The user question is empty.")

    config = load_config()
    deps = dependencies or AgentDependencies()
    llm_client = deps.llm_client or OpenRouterClient(config)
    legal_tool = deps.legal_tool or LegalRetrievalAdapter()
    search_tool = deps.search_tool or DuckDuckGoSearchTool(
        max_results=config.web_search_max_results
    )
    scraper_tool = deps.scraper_tool or WebScraperTool(
        timeout_seconds=config.scraper_timeout_seconds,
        max_chars=config.scraper_max_chars,
    )

    legal_issues = _identify_legal_issues(question, llm_client)
    legal_basis = legal_tool.retrieve(question)
    search_query = build_practical_search_query(question, legal_issues)
    search_results = search_tool.search(search_query)
    practical_references = _scrape_practical_references(search_results, scraper_tool)

    try:
        synthesized = _synthesize_final_json(
            question=question,
            legal_issues=legal_issues,
            legal_basis=legal_basis,
            practical_references=practical_references,
            llm_client=llm_client,
        )
        return normalize_agent_response(synthesized)
    except Exception as exc:
        return normalize_agent_response(
            _fallback_from_evidence(
                question=question,
                legal_issues=legal_issues,
                legal_basis=legal_basis,
                practical_references=practical_references,
                reason=str(exc),
            )
        )


def _identify_legal_issues(question: str, llm_client: Any) -> list[str]:
    try:
        response = llm_client.complete(
            [
                {
                    "role": "system",
                    "content": "Extract 2-5 short labor-law issue labels as JSON array.",
                },
                {"role": "user", "content": question},
            ],
            json_mode=True,
            max_tokens=250,
        )
        parsed = json.loads(response)
        if isinstance(parsed, list):
            return [str(item) for item in parsed[:5]]
        if isinstance(parsed, dict) and isinstance(parsed.get("legal_issues"), list):
            return [str(item) for item in parsed["legal_issues"][:5]]
    except (LLMClientError, json.JSONDecodeError, TypeError, ValueError):
        pass

    return _simple_issue_fallback(question)


def _simple_issue_fallback(question: str) -> list[str]:
    lowered = question.lower()
    issues: list[str] = []
    keyword_map = {
        "salary or unpaid wage": ["salary", "lương", "wage", "paid"],
        "forced resignation": ["resignation", "nghỉ việc", "ký đơn"],
        "dismissal or termination": ["dismiss", "terminate", "sa thải", "chấm dứt"],
        "probation": ["probation", "thử việc"],
        "maternity protection": ["pregnant", "pregnancy", "thai sản", "mang thai"],
        "social insurance": ["insurance", "bảo hiểm"],
    }
    for label, keywords in keyword_map.items():
        if any(keyword in lowered for keyword in keywords):
            issues.append(label)
    return issues or ["labor-law issue"]


def _scrape_practical_references(
    search_results: list[dict[str, str]],
    scraper_tool: WebScraperTool,
) -> list[dict[str, str]]:
    references: list[dict[str, str]] = []
    for result in search_results:
        url = result.get("url", "")
        if not url or result.get("status") == "failed":
            continue
        scraped = scraper_tool.scrape(url)
        if scraped.get("status") != "success":
            continue
        references.append(
            {
                "title": scraped.get("title") or result.get("title", ""),
                "url": url,
                "summary": scraped.get("content_excerpt", "")[:700],
            }
        )
        if len(references) >= 3:
            break
    return references


def _synthesize_final_json(
    *,
    question: str,
    legal_issues: list[str],
    legal_basis: list[dict[str, str]],
    practical_references: list[dict[str, str]],
    llm_client: Any,
) -> dict[str, Any]:
    prompt = {
        "question": question,
        "legal_issues": legal_issues,
        "legal_basis": legal_basis,
        "practical_references": practical_references,
        "required_schema": [
            "case_summary",
            "legal_issues",
            "legal_basis",
            "practical_references",
            "recommendations",
            "limitations",
        ],
    }
    response = llm_client.complete(
        [
            {
                "role": "system",
                "content": (
                    "Return only valid JSON. Do not invent legal basis. "
                    "Web references are practical examples only."
                ),
            },
            {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
        ],
        json_mode=True,
    )
    parsed = json.loads(response)
    if not isinstance(parsed, dict):
        raise ValueError("LLM returned JSON that is not an object.")
    return parsed


def _fallback_from_evidence(
    *,
    question: str,
    legal_issues: list[str],
    legal_basis: list[dict[str, str]],
    practical_references: list[dict[str, str]],
    reason: str,
) -> dict[str, Any]:
    response = fallback_response(question, reason)
    response["legal_issues"] = legal_issues
    response["legal_basis"] = legal_basis
    response["practical_references"] = practical_references
    if legal_basis:
        response["recommendations"] = [
            {
                "option": "Review the retrieved legal basis",
                "when_to_use": "Use this before choosing an escalation path.",
                "suggested_steps": [
                    "Compare your facts with the retrieved legal excerpts.",
                    "Collect documents that prove the timeline and employment relationship.",
                    "Ask HR, a labor authority, or a lawyer for case-specific review.",
                ],
            }
        ]
    return response
