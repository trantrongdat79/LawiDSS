"""Smoke test for OpenRouter connectivity.

Run only after creating a local .env file with OPENROUTER_API_KEY.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.agent.llm_client import LLMClientError, OpenRouterClient


def main() -> int:
    client = OpenRouterClient.from_env()
    try:
        response = client.complete(
            [{"role": "user", "content": "Reply with exactly: OK"}],
            max_tokens=10,
        )
    except LLMClientError as exc:
        print(f"OpenRouter smoke test failed: {exc}")
        return 1

    print("OpenRouter smoke test succeeded.")
    print(f"Model response: {response[:80]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
