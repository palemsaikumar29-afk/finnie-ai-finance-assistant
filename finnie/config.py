"""Central configuration. All secrets come from environment variables only.

Required for full functionality:
    OPENAI_API_KEY        Chat/completion model for router + agents
Optional (tools degrade to mock data when missing):
    TAVILY_API_KEY        News search
    SERPAPI_API_KEY       News search fallback
    ALPHA_VANTAGE_API_KEY Live market quotes
"""
from __future__ import annotations

import os


def _sanitize_proxy_env() -> None:
    """Drop IPv6 literals from no_proxy that crash httpx-based clients.

    Some runtimes export IPv6 addresses (e.g. ``::1``, ``[::1]``) in
    no_proxy. httpx (used by huggingface_hub) turns each entry into a
    mount pattern like ``all://*[::1]`` which its own URLPattern parser
    then rejects with ``InvalidURL: Invalid port``. IPv6 loopback entries
    are irrelevant for this app's outbound API calls, so they are removed;
    everything else is left untouched.
    """
    for var in ("no_proxy", "NO_PROXY"):
        raw = os.environ.get(var)
        if not raw:
            continue
        kept = [
            entry.strip()
            for entry in raw.split(",")
            if ":" not in entry  # drop IPv6 literals, keep hostnames/IPv4
        ]
        os.environ[var] = ",".join(e for e in kept if e)


_sanitize_proxy_env()


class Settings:
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    TAVILY_API_KEY: str | None = os.getenv("TAVILY_API_KEY")
    SERPAPI_API_KEY: str | None = os.getenv("SERPAPI_API_KEY")
    ALPHA_VANTAGE_API_KEY: str | None = os.getenv("ALPHA_VANTAGE_API_KEY")

    LLM_MODEL: str = os.getenv("FINNIE_LLM_MODEL", "gpt-4o-mini")
    EMBEDDING_MODEL: str = os.getenv(
        "FINNIE_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )
    # Alpha Vantage free tier is 25 requests/day — cache aggressively.
    QUOTE_CACHE_TTL_SECONDS: int = int(os.getenv("FINNIE_QUOTE_TTL", "1800"))
    RAG_TOP_K: int = int(os.getenv("FINNIE_RAG_TOP_K", "4"))

    @property
    def llm_available(self) -> bool:
        return bool(self.OPENAI_API_KEY)

    @property
    def news_search_available(self) -> bool:
        return bool(self.TAVILY_API_KEY or self.SERPAPI_API_KEY)

    @property
    def live_quotes_available(self) -> bool:
        return bool(self.ALPHA_VANTAGE_API_KEY)


settings = Settings()
