"""DuckDuckGo search tool interface for practical references."""

from __future__ import annotations

import html
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any, Callable


SearchProvider = Callable[[str, int], list[dict[str, Any]]]


@dataclass
class DuckDuckGoSearchTool:
    """Small, testable DuckDuckGo HTML search adapter.

    The provider injection keeps unit tests offline. The default provider uses
    DuckDuckGo's lightweight HTML endpoint and should be treated as a best-effort
    development helper, not a guaranteed production API.
    """

    max_results: int = 5
    provider: SearchProvider | None = None

    def search(self, query: str) -> list[dict[str, str]]:
        """Search practical references and return structured results."""

        query = query.strip()
        if not query:
            return []

        try:
            if self.provider:
                raw_results = self.provider(query, self.max_results)
            else:
                raw_results = self._duckduckgo_html_search(query)
        except Exception as exc:  # pragma: no cover - defensive runtime path
            return [
                {
                    "title": "",
                    "url": "",
                    "snippet": "",
                    "status": "failed",
                    "error": str(exc),
                }
            ]

        return [normalize_search_result(item) for item in raw_results[: self.max_results]]

    def _duckduckgo_html_search(self, query: str) -> list[dict[str, str]]:
        encoded = urllib.parse.urlencode({"q": query})
        request = urllib.request.Request(
            f"https://html.duckduckgo.com/html/?{encoded}",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        with urllib.request.urlopen(request, timeout=15) as response:
            page = response.read().decode("utf-8", errors="replace")

        results: list[dict[str, str]] = []
        pattern = re.compile(
            r'<a rel="nofollow" class="result__a" href="(?P<url>.*?)".*?>(?P<title>.*?)</a>',
            re.DOTALL,
        )
        for match in pattern.finditer(page):
            title = re.sub("<.*?>", "", match.group("title"))
            url = html.unescape(match.group("url"))
            results.append(
                {
                    "title": html.unescape(title).strip(),
                    "url": _decode_duckduckgo_url(url),
                    "snippet": "",
                    "status": "success",
                }
            )
            if len(results) >= self.max_results:
                break
        return results


def normalize_search_result(item: dict[str, Any]) -> dict[str, str]:
    """Normalize a search result for downstream scraping."""

    return {
        "title": str(item.get("title") or ""),
        "url": str(item.get("url") or ""),
        "snippet": str(item.get("snippet") or ""),
        "status": str(item.get("status") or "success"),
        **({"error": str(item.get("error"))} if item.get("error") else {}),
    }


def build_practical_search_query(question: str, legal_issues: list[str]) -> str:
    """Build a concise Vietnamese search query for practical references."""

    issue_text = " ".join(legal_issues[:3]).strip()
    base = issue_text or question
    return f"{base} tranh chấp lao động người lao động Việt Nam"


def _decode_duckduckgo_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)
    if "uddg" in params and params["uddg"]:
        return params["uddg"][0]
    return url
