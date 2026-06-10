from src.agent.schemas.output_schema import (
    fallback_response,
    is_valid_agent_response,
    normalize_agent_response,
)


def test_normalize_adds_missing_fields():
    response = normalize_agent_response({"case_summary": "Test"})

    assert response["case_summary"] == "Test"
    assert response["legal_issues"] == []
    assert response["legal_basis"] == []
    assert response["practical_references"] == []
    assert response["recommendations"] == []
    assert response["limitations"]


def test_normalize_repairs_wrong_list_types():
    response = normalize_agent_response(
        {
            "case_summary": "Test",
            "legal_issues": "not-a-list",
            "legal_basis": "not-a-list",
            "practical_references": "not-a-list",
            "recommendations": "not-a-list",
        }
    )

    assert response["legal_issues"] == []
    assert response["legal_basis"] == []
    assert response["practical_references"] == []
    assert response["recommendations"] == []


def test_fallback_response_is_valid():
    response = fallback_response("Question", "Testing fallback")

    assert is_valid_agent_response(response)
    assert "Testing fallback" in response["limitations"]
