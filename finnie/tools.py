"""External tools with graceful degradation.

Design rule: an absent API key (or a failed request) must NEVER crash the
app — every tool falls back to realistic mock data and flags the result as
``source: "mock"`` so the UI can be transparent about it.
"""
from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field

import requests

from finnie.config import settings


# ---------------------------------------------------------------------------
# Quote cache (Alpha Vantage free tier is 25 requests/day — the "#1 demo killer")
# ---------------------------------------------------------------------------
@dataclass
class _CacheEntry:
    value: dict
    expires_at: float


_quote_cache: dict[str, _CacheEntry] = {}


def _cache_get(symbol: str) -> dict | None:
    entry = _quote_cache.get(symbol.upper())
    if entry and entry.expires_at > time.time():
        return entry.value
    _quote_cache.pop(symbol.upper(), None)
    return None


def _cache_set(symbol: str, value: dict) -> None:
    _quote_cache[symbol.upper()] = _CacheEntry(
        value=value, expires_at=time.time() + settings.QUOTE_CACHE_TTL_SECONDS
    )


# Realistic mock quotes used when no key is present or the API errors.
MOCK_QUOTES: dict[str, dict] = {
    "AAPL": {"price": 232.40, "change_pct": 0.85, "name": "Apple Inc."},
    "MSFT": {"price": 428.15, "change_pct": -0.32, "name": "Microsoft Corp."},
    "GOOGL": {"price": 176.33, "change_pct": 1.12, "name": "Alphabet Inc."},
    "AMZN": {"price": 195.02, "change_pct": 0.44, "name": "Amazon.com Inc."},
    "TSLA": {"price": 248.90, "change_pct": -1.75, "name": "Tesla Inc."},
    "NVDA": {"price": 131.88, "change_pct": 2.31, "name": "NVIDIA Corp."},
    "SPY": {"price": 573.20, "change_pct": 0.52, "name": "SPDR S&P 500 ETF"},
    "QQQ": {"price": 498.75, "change_pct": 0.91, "name": "Invesco QQQ Trust"},
    "VOO": {"price": 526.10, "change_pct": 0.50, "name": "Vanguard S&P 500 ETF"},
    "BND": {"price": 73.44, "change_pct": 0.06, "name": "Vanguard Total Bond ETF"},
}


def _mock_quote(symbol: str) -> dict:
    sym = symbol.upper()
    base = MOCK_QUOTES.get(sym)
    if base:
        return {"symbol": sym, **base, "source": "mock"}
    # Deterministic pseudo-quote for unknown symbols so demos stay stable.
    seed = sum(ord(c) for c in sym) % 1000
    return {
        "symbol": sym,
        "name": f"{sym} (mock data)",
        "price": round(20 + seed / 5, 2),
        "change_pct": round(((seed % 40) - 20) / 10, 2),
        "source": "mock",
    }


def _alpha_vantage_quote_sync(symbol: str) -> dict | None:
    """Blocking Alpha Vantage call — always run in a thread."""
    try:
        resp = requests.get(
            "https://www.alphavantage.co/query",
            params={
                "function": "GLOBAL_QUOTE",
                "symbol": symbol.upper(),
                "apikey": settings.ALPHA_VANTAGE_API_KEY,
            },
            timeout=10,
        )
        data = resp.json().get("Global Quote", {})
        price = data.get("05. price")
        if not price:
            return None
        return {
            "symbol": symbol.upper(),
            "name": symbol.upper(),
            "price": round(float(price), 2),
            "change_pct": round(
                float(data.get("10. change percent", "0%").rstrip("%")), 2
            ),
            "source": "alpha_vantage",
        }
    except Exception:
        return None


async def get_quote(symbol: str) -> dict:
    """Live quote with 30-min TTL cache; falls back to mock data."""
    cached = _cache_get(symbol)
    if cached is not None:
        return {**cached, "cached": True}

    result: dict | None = None
    if settings.live_quotes_available:
        result = await asyncio.to_thread(_alpha_vantage_quote_sync, symbol)
    if result is None:
        result = _mock_quote(symbol)
    result["cached"] = False
    _cache_set(symbol, result)
    return dict(result)


# ---------------------------------------------------------------------------
# News search (Tavily -> SerpApi -> mock)
# ---------------------------------------------------------------------------
MOCK_NEWS: list[dict] = [
    {
        "title": "S&P 500 extends gains as tech earnings beat expectations",
        "source": "MarketWire (mock)",
        "snippet": "Major indexes climbed as large-cap tech reported stronger-than-expected "
        "results, with analysts noting resilient consumer spending.",
    },
    {
        "title": "Fed holds rates steady, signals data-dependent path",
        "source": "MarketWire (mock)",
        "snippet": "The Federal Reserve kept its benchmark rate unchanged, reiterating that "
        "future moves will depend on incoming inflation and labor data.",
    },
    {
        "title": "ETF inflows hit record as investors favor low-cost index funds",
        "source": "MarketWire (mock)",
        "snippet": "Investors poured a record sum into ETFs this quarter, continuing the "
        "long-running shift from high-fee active mutual funds.",
    },
]


def _tavily_search_sync(query: str, max_results: int = 5) -> list[dict] | None:
    try:
        resp = requests.post(
            "https://api.tavily.com/search",
            json={"api_key": settings.TAVILY_API_KEY, "query": query,
                  "max_results": max_results, "search_depth": "basic"},
            timeout=12,
        )
        items = resp.json().get("results", [])
        return [
            {"title": r.get("title", ""), "source": r.get("url", ""),
             "snippet": (r.get("content") or "")[:400]}
            for r in items
        ] or None
    except Exception:
        return None


def _serpapi_search_sync(query: str, max_results: int = 5) -> list[dict] | None:
    try:
        resp = requests.get(
            "https://serpapi.com/search.json",
            params={"engine": "google_news", "q": query,
                    "api_key": settings.SERPAPI_API_KEY},
            timeout=12,
        )
        items = resp.json().get("news_results", [])[:max_results]
        return [
            {"title": r.get("title", ""), "source": r.get("source", {}).get("name", ""),
             "snippet": r.get("snippet", "")}
            for r in items
        ] or None
    except Exception:
        return None


async def search_news(query: str, max_results: int = 5) -> dict:
    """News search; returns {'results': [...], 'source': 'tavily'|'serpapi'|'mock'}."""
    results, source = None, "mock"
    if settings.TAVILY_API_KEY:
        results = await asyncio.to_thread(_tavily_search_sync, query, max_results)
        source = "tavily"
    if not results and settings.SERPAPI_API_KEY:
        results = await asyncio.to_thread(_serpapi_search_sync, query, max_results)
        source = "serpapi"
    if not results:
        results, source = list(MOCK_NEWS), "mock"
    return {"results": results[:max_results], "source": source}


# ---------------------------------------------------------------------------
# Portfolio math helpers
# ---------------------------------------------------------------------------
def compound_growth(monthly: float, annual_rate_pct: float, years: int) -> float:
    """Future value of monthly contributions with monthly compounding."""
    r = annual_rate_pct / 100 / 12
    n = years * 12
    if r <= 0:
        return monthly * n
    return monthly * ((1 + r) ** n - 1) / r


def portfolio_summary(positions: list[dict], prices: dict[str, float]) -> dict:
    """positions: [{symbol, shares, avg_cost}], prices: {symbol: price}."""
    rows, total_value, total_cost = [], 0.0, 0.0
    for p in positions:
        sym = p["symbol"].upper()
        price = prices.get(sym, 0.0)
        value = p["shares"] * price
        cost = p["shares"] * p["avg_cost"]
        pnl = value - cost
        rows.append({
            "symbol": sym, "shares": p["shares"], "avg_cost": p["avg_cost"],
            "price": round(price, 2), "value": round(value, 2),
            "pnl": round(pnl, 2),
            "pnl_pct": round(pnl / cost * 100, 2) if cost else 0.0,
        })
        total_value += value
        total_cost += cost
    for row in rows:
        row["weight_pct"] = round(row["value"] / total_value * 100, 2) if total_value else 0.0
    return {
        "positions": rows,
        "total_value": round(total_value, 2),
        "total_cost": round(total_cost, 2),
        "total_pnl": round(total_value - total_cost, 2),
        "total_pnl_pct": round((total_value - total_cost) / total_cost * 100, 2)
        if total_cost else 0.0,
    }


DEFAULT_PORTFOLIO: list[dict] = [
    {"symbol": "VOO", "shares": 40, "avg_cost": 470.00},
    {"symbol": "QQQ", "shares": 25, "avg_cost": 440.00},
    {"symbol": "AAPL", "shares": 30, "avg_cost": 190.00},
    {"symbol": "MSFT", "shares": 15, "avg_cost": 380.00},
    {"symbol": "BND", "shares": 60, "avg_cost": 72.00},
]
