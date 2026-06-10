"""Adapter for Member 1's future legal retrieval tool."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


class QueryEngineProtocol(Protocol):
    """Minimal interface expected from Member 1's QueryEngineTool."""

    def query(self, question: str, top_k: int = 3) -> list[dict[str, Any]]:
        """Return legal retrieval results."""


@dataclass
class LegalRetrievalAdapter:
    """Normalize Member 1 legal retrieval results for Member 2."""

    query_engine: QueryEngineProtocol | None = None
    mock_results: list[dict[str, Any]] | None = None
    top_k: int = 3

    def retrieve(self, question: str) -> list[dict[str, str]]:
        """Retrieve and normalize legal basis."""

        if self.mock_results is not None:
            raw_results = self.mock_results
        elif self.query_engine is not None:
            raw_results = self.query_engine.query(question, top_k=self.top_k)
        else:
            raw_results = []

        return [normalize_legal_result(item) for item in raw_results[: self.top_k]]


def normalize_legal_result(item: dict[str, Any]) -> dict[str, str]:
    """Normalize one legal retrieval result to the agreed JSON shape."""

    return {
        "document_name": str(
            item.get("document_name") or item.get("document") or item.get("title") or ""
        ),
        "article": str(item.get("article") or item.get("clause") or ""),
        "effective_status": str(
            item.get("effective_status") or item.get("status") or ""
        ),
        "excerpt": str(item.get("excerpt") or item.get("text") or item.get("content") or ""),
        "source": str(item.get("source") or item.get("url") or ""),
    }
