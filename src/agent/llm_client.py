"""OpenRouter client isolated behind a small project-local interface."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

from src.agent.config import AgentConfig, load_config


class LLMClientError(RuntimeError):
    """Raised when the OpenRouter client cannot complete a request."""


@dataclass
class OpenRouterClient:
    """Small direct HTTP client for OpenRouter chat completions."""

    config: AgentConfig

    @classmethod
    def from_env(cls) -> "OpenRouterClient":
        return cls(load_config())

    def complete(
        self,
        messages: list[dict[str, str]],
        *,
        json_mode: bool = False,
        max_tokens: int | None = None,
    ) -> str:
        """Call OpenRouter and return assistant text content."""

        if not self.config.openrouter_api_key:
            raise LLMClientError(
                "OPENROUTER_API_KEY is missing. Copy .env.example to .env and add a key."
            )

        payload: dict[str, Any] = {
            "model": self.config.openrouter_model,
            "messages": messages,
            "temperature": self.config.llm_temperature,
            "max_tokens": max_tokens or self.config.llm_max_tokens,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        url = self.config.openrouter_base_url.rstrip("/") + "/chat/completions"
        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.config.openrouter_api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost",
                "X-OpenRouter-Title": "DSS Labor Law Project",
            },
        )

        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                response_body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            raise LLMClientError(f"OpenRouter HTTP {exc.code}: {error_body}") from exc
        except urllib.error.URLError as exc:
            raise LLMClientError(f"Could not reach OpenRouter: {exc.reason}") from exc
        except TimeoutError as exc:
            raise LLMClientError("OpenRouter request timed out.") from exc

        try:
            parsed = json.loads(response_body)
            content = parsed["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            raise LLMClientError(f"Invalid OpenRouter response: {response_body}") from exc

        if not content:
            raise LLMClientError("OpenRouter returned an empty assistant response.")

        return str(content)


class MockLLMClient:
    """Deterministic test double for unit tests and offline development."""

    def __init__(self, response: str):
        self.response = response
        self.calls: list[list[dict[str, str]]] = []

    def complete(
        self,
        messages: list[dict[str, str]],
        *,
        json_mode: bool = False,
        max_tokens: int | None = None,
    ) -> str:
        self.calls.append(messages)
        return self.response
