"""Web scraper tool for practical reference pages."""

from __future__ import annotations

import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Callable


@dataclass
class WebScraperTool:
    """Fetch and extract readable text from a URL."""

    timeout_seconds: int = 10
    max_chars: int = 4000
    fetcher: Callable[[str], str] | None = None

    def scrape(self, url: str) -> dict[str, str]:
        """Return title and readable content excerpt for a URL."""

        if not _is_http_url(url):
            return _failed(url, "Invalid URL. Only http and https URLs are supported.")

        try:
            html = self.fetcher(url) if self.fetcher else self._fetch(url)
        except TimeoutError:
            return _failed(url, "Request timed out.")
        except urllib.error.URLError as exc:
            return _failed(url, f"Could not fetch URL: {exc.reason}")
        except Exception as exc:  # pragma: no cover - defensive runtime path
            return _failed(url, f"Could not fetch URL: {exc}")

        title, text = extract_readable_text(html)
        excerpt = text[: self.max_chars].strip()
        if not title and not excerpt:
            return _failed(url, "Could not extract readable content.")

        return {
            "title": title,
            "url": url,
            "content_excerpt": excerpt,
            "status": "success",
        }

    def _fetch(self, url: str) -> str:
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
            return response.read().decode("utf-8", errors="replace")


class _ReadableTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title_parts: list[str] = []
        self.text_parts: list[str] = []
        self._skip_depth = 0
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "nav", "footer", "header", "noscript"}:
            self._skip_depth += 1
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "nav", "footer", "header", "noscript"}:
            self._skip_depth = max(0, self._skip_depth - 1)
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        cleaned = " ".join(data.split())
        if not cleaned:
            return
        if self._in_title:
            self.title_parts.append(cleaned)
        elif self._skip_depth == 0:
            self.text_parts.append(cleaned)


def extract_readable_text(html: str) -> tuple[str, str]:
    """Extract a simple title and readable text from HTML."""

    parser = _ReadableTextParser()
    parser.feed(html)
    title = " ".join(parser.title_parts).strip()
    text = " ".join(parser.text_parts)
    text = re.sub(r"\s+", " ", text).strip()
    return title, text


def _is_http_url(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _failed(url: str, error: str) -> dict[str, str]:
    return {
        "title": "",
        "url": url,
        "content_excerpt": "",
        "status": "failed",
        "error": error,
    }
