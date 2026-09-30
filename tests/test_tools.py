"""Tool tests — all run without API keys (mock fallback + math)."""
import asyncio
import time

import finnie.config as cfg
import finnie.tools as tools


def _offline():
    for attr in ("OPENAI_API_KEY", "TAVILY_API_KEY", "SERPAPI_API_KEY", "ALPHA_VANTAGE_API_KEY"):
        setattr(cfg.settings, attr, None)


def test_get_quote_mock_fallback():
    _offline()
    q = asyncio.run(tools.get_quote("AAPL"))
    assert q["symbol"] == "AAPL"
    assert q["source"] == "mock"
    assert q["price"] > 0


def test_get_quote_unknown_symbol_mock():
    _offline()
    q = asyncio.run(tools.get_quote("ZZZZ"))
    assert q["source"] == "mock" and q["price"] > 0


def test_quote_cache_ttl():
    _offline()
    tools._quote_cache.clear()
    first = asyncio.run(tools.get_quote("MSFT"))
    assert first["cached"] is False
    second = asyncio.run(tools.get_quote("MSFT"))
    assert second["cached"] is True
    assert second["price"] == first["price"]
    # Expire the entry and confirm a fresh fetch happens.
    tools._quote_cache["MSFT"].expires_at = time.time() - 1
    third = asyncio.run(tools.get_quote("MSFT"))
    assert third["cached"] is False


def test_search_news_mock_fallback():
    _offline()
    res = asyncio.run(tools.search_news("markets"))
    assert res["source"] == "mock"
    assert len(res["results"]) >= 1
    assert "title" in res["results"][0]


def test_compound_growth():
    # $500/mo @ 7% for 30y ≈ $609k
    fv = tools.compound_growth(500, 7.0, 30)
    assert 590_000 < fv < 630_000
    # Zero rate = plain sum
    assert tools.compound_growth(100, 0, 1) == 1200


def test_lump_sum_growth():
    # $10,000 x 1.07^10 = $19,671.51 (regression: the T1 failing input)
    fv = tools.lump_sum_growth(10000, 7.0, 10)
    assert abs(fv - 19671.51) < 0.01
    # Zero rate = principal back
    assert tools.lump_sum_growth(1000, 0, 5) == 1000
    # Fractional years handled
    assert tools.lump_sum_growth(1000, 10.0, 0.5) > 1000


def test_portfolio_summary_math():
    positions = [{"symbol": "AAPL", "shares": 10, "avg_cost": 100.0}]
    s = tools.portfolio_summary(positions, {"AAPL": 150.0})
    assert s["total_value"] == 1500.0
    assert s["total_pnl"] == 500.0
    assert s["total_pnl_pct"] == 50.0
    assert s["positions"][0]["weight_pct"] == 100.0


def test_market_agent_ticker_extraction():
    import finnie.agents as agents
    import finnie.config as cfg

    cfg.settings.OPENAI_API_KEY = None
    cfg.settings.ALPHA_VANTAGE_API_KEY = None
    out = asyncio.run(agents.market_agent("What is the price of AAPL?", {}))
    assert "AAPL" in out
    assert "WHAT" not in out and "PRICE" not in out


def test_portfolio_agent_runs_offline():
    import finnie.agents as agents
    import finnie.config as cfg

    cfg.settings.OPENAI_API_KEY = None
    cfg.settings.ALPHA_VANTAGE_API_KEY = None
    out = asyncio.run(agents.portfolio_agent("Analyze my portfolio", {}))
    assert "Total value" in out
    assert "mock" in out.lower()
