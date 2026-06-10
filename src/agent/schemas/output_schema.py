"""Validation helpers for the Agent's frontend-facing JSON output."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


REQUIRED_TOP_LEVEL_FIELDS = {
    "case_summary": "",
    "legal_issues": [],
    "legal_basis": [],
    "practical_references": [],
    "recommendations": [],
    "limitations": (
        "This system is for decision support only and does not replace official "
        "legal advice from a lawyer or competent authority."
    ),
}

LEGAL_BASIS_FIELDS = {
    "document_name": "",
    "article": "",
    "effective_status": "",
    "excerpt": "",
    "source": "",
}

PRACTICAL_REFERENCE_FIELDS = {
    "title": "",
    "url": "",
    "summary": "",
}

RECOMMENDATION_FIELDS = {
    "option": "",
    "when_to_use": "",
    "suggested_steps": [],
}


def fallback_response(question: str, reason: str) -> dict[str, Any]:
    """Return a safe JSON response when the Agent cannot complete normally."""

    response = deepcopy(REQUIRED_TOP_LEVEL_FIELDS)
    response["case_summary"] = question.strip() or "No user question was provided."
    response["legal_issues"] = []
    response["legal_basis"] = []
    response["practical_references"] = []
    response["recommendations"] = [
        {
            "option": "Collect more information",
            "when_to_use": "Use this when the system cannot retrieve enough reliable evidence.",
            "suggested_steps": [
                "Write down the timeline of events.",
                "Collect contracts, messages, payslips, and official documents.",
                "Ask a lawyer or competent authority to review the case.",
            ],
        }
    ]
    response["limitations"] = (
        f"{REQUIRED_TOP_LEVEL_FIELDS['limitations']} Reason: {reason}"
    )
    return response


def normalize_agent_response(value: dict[str, Any]) -> dict[str, Any]:
    """Normalize an Agent response so Member 3 can render it safely."""

    normalized = deepcopy(REQUIRED_TOP_LEVEL_FIELDS)
    normalized.update(value)

    normalized["case_summary"] = str(normalized.get("case_summary") or "")
    normalized["limitations"] = str(
        normalized.get("limitations") or REQUIRED_TOP_LEVEL_FIELDS["limitations"]
    )

    legal_issues = normalized.get("legal_issues")
    normalized["legal_issues"] = legal_issues if isinstance(legal_issues, list) else []

    normalized["legal_basis"] = [
        _normalize_item(item, LEGAL_BASIS_FIELDS)
        for item in _as_list(normalized.get("legal_basis"))
    ]
    normalized["practical_references"] = [
        _normalize_item(item, PRACTICAL_REFERENCE_FIELDS)
        for item in _as_list(normalized.get("practical_references"))
    ]
    normalized["recommendations"] = [
        _normalize_recommendation(item)
        for item in _as_list(normalized.get("recommendations"))
    ]

    return normalized


def is_valid_agent_response(value: Any) -> bool:
    """Return True when a value can be safely used as Agent JSON output."""

    if not isinstance(value, dict):
        return False
    normalized = normalize_agent_response(value)
    return all(field in normalized for field in REQUIRED_TOP_LEVEL_FIELDS)


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _normalize_item(value: Any, template: dict[str, Any]) -> dict[str, Any]:
    output = deepcopy(template)
    if isinstance(value, dict):
        output.update({key: value.get(key, default) for key, default in template.items()})
    return output


def _normalize_recommendation(value: Any) -> dict[str, Any]:
    item = _normalize_item(value, RECOMMENDATION_FIELDS)
    if not isinstance(item["suggested_steps"], list):
        item["suggested_steps"] = []
    return item
