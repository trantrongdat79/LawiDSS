import json

from src.agent.agent_workflow import AgentDependencies, answer_labor_law_question
from src.agent.llm_client import MockLLMClient
from src.agent.schemas.output_schema import is_valid_agent_response
from src.agent.tools.legal_retrieval_tool import LegalRetrievalAdapter
from src.agent.tools.web_scraper_tool import WebScraperTool
from src.agent.tools.web_search_tool import DuckDuckGoSearchTool


def _deps(llm_response: dict):
    llm = MockLLMClient(json.dumps(llm_response))
    legal_tool = LegalRetrievalAdapter(
        mock_results=[
            {
                "document_name": "Labor Code",
                "article": "Article 94",
                "effective_status": "Effective",
                "excerpt": "Employers must pay wages fully and on time.",
                "source": "mock://law",
            }
        ]
    )
    search_tool = DuckDuckGoSearchTool(
        provider=lambda query, max_results: [
            {
                "title": "Unpaid salary case",
                "url": "https://example.com/case",
                "snippet": "A worker salary case.",
            }
        ]
    )
    scraper = WebScraperTool(
        fetcher=lambda url: "<title>Case</title><article>Worker collected evidence.</article>"
    )
    return AgentDependencies(
        llm_client=llm,
        legal_tool=legal_tool,
        search_tool=search_tool,
        scraper_tool=scraper,
    )


def test_agent_workflow_happy_path():
    response = answer_labor_law_question(
        "My company has not paid salary for 2 months.",
        _deps(
            {
                "case_summary": "The user reports unpaid salary.",
                "legal_issues": ["unpaid salary"],
                "legal_basis": [
                    {
                        "document_name": "Labor Code",
                        "article": "Article 94",
                        "effective_status": "Effective",
                        "excerpt": "Employers must pay wages fully and on time.",
                        "source": "mock://law",
                    }
                ],
                "practical_references": [
                    {
                        "title": "Case",
                        "url": "https://example.com/case",
                        "summary": "Worker collected evidence.",
                    }
                ],
                "recommendations": [
                    {
                        "option": "Send a written salary request",
                        "when_to_use": "When salary is overdue.",
                        "suggested_steps": ["Collect payslips", "Send written request"],
                    }
                ],
                "limitations": "Decision support only.",
            }
        ),
    )

    assert is_valid_agent_response(response)
    assert response["legal_basis"][0]["article"] == "Article 94"


def test_agent_workflow_empty_input():
    response = answer_labor_law_question("")

    assert is_valid_agent_response(response)
    assert "empty" in response["limitations"].lower()


def test_agent_workflow_empty_legal_retrieval_is_cautious():
    deps = _deps({"not": "the expected schema"})
    deps.legal_tool = LegalRetrievalAdapter(mock_results=[])

    response = answer_labor_law_question("Can I sue?", deps)

    assert is_valid_agent_response(response)
    assert response["legal_basis"] == []


def test_agent_workflow_web_search_failure_still_returns_json():
    deps = _deps({"not": "the expected schema"})
    deps.search_tool = DuckDuckGoSearchTool(
        provider=lambda query, max_results: [
            {"status": "failed", "error": "search unavailable"}
        ]
    )

    response = answer_labor_law_question("My salary is unpaid.", deps)

    assert is_valid_agent_response(response)
    assert response["practical_references"] == []
