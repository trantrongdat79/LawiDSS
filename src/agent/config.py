"""Configuration helpers for Member 2's Agentic RAG workflow."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ENV_PATH = PROJECT_ROOT / ".env"


def load_env_file(path: Path = DEFAULT_ENV_PATH) -> None:
    """Load simple KEY=VALUE pairs from a local .env file if it exists."""

    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _get_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    try:
        return float(value)
    except ValueError:
        return default


@dataclass(frozen=True)
class AgentConfig:
    """Runtime configuration for OpenRouter and Agent tools."""

    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "openrouter/free"
    llm_temperature: float = 0.2
    llm_max_tokens: int = 1200
    web_search_max_results: int = 5
    scraper_timeout_seconds: int = 10
    scraper_max_chars: int = 4000


def load_config() -> AgentConfig:
    """Load config from .env and environment variables."""

    load_env_file()
    return AgentConfig(
        openrouter_api_key=os.getenv("OPENROUTER_API_KEY", ""),
        openrouter_base_url=os.getenv(
            "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
        ),
        openrouter_model=os.getenv("OPENROUTER_MODEL", "openrouter/free"),
        llm_temperature=_get_float("LLM_TEMPERATURE", 0.2),
        llm_max_tokens=_get_int("LLM_MAX_TOKENS", 1200),
        web_search_max_results=_get_int("WEB_SEARCH_MAX_RESULTS", 5),
        scraper_timeout_seconds=_get_int("SCRAPER_TIMEOUT_SECONDS", 10),
        scraper_max_chars=_get_int("SCRAPER_MAX_CHARS", 4000),
    )
