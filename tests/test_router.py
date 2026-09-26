"""Router tests — use the deterministic keyword classifier (no LLM needed)."""
import asyncio

from finnie.graph import classify_sync, run_finnie


def test_classify_sync_tax():
    assert classify_sync("How are capital gains taxed?") == "tax_education"
    assert classify_sync("Explain the wash sale rule") == "tax_education"


def test_classify_sync_portfolio():
    assert classify_sync("How is my portfolio allocated?") == "portfolio"
    assert classify_sync("What are my holdings?") == "portfolio"


def test_classify_sync_market():
    assert classify_sync("What is the price of AAPL?") == "market"
    assert classify_sync("Give me a quote for NVDA") == "market"


def test_classify_sync_goals():
    assert classify_sync("I want $1 million in 20 years") == "goals"
    assert classify_sync("How much should I save for retirement?") == "goals"


def test_classify_sync_news():
    assert classify_sync("Latest news on the Fed") == "news"
    assert classify_sync("What are today's market headlines?") == "news"


def test_classify_sync_default_finance_qa():
    assert classify_sync("What is compound interest?") == "finance_qa"
    assert classify_sync("Explain ETFs") == "finance_qa"


def test_run_finnie_routes_and_answers():
    # Force offline mode so the test is hermetic.
    import finnie.config as cfg

    orig = cfg.settings.OPENAI_API_KEY
    cfg.settings.OPENAI_API_KEY = None
    try:
        result = asyncio.run(run_finnie("What is dollar-cost averaging?"))
        assert result["route"] == "finance_qa"
        assert "dollar" in result["answer"].lower() or "cost" in result["answer"].lower()

        result = asyncio.run(run_finnie("I want $500k in 15 years"))
        assert result["route"] == "goals"
        assert "500,000" in result["answer"] or "500000" in result["answer"]

        result = asyncio.run(run_finnie("Explain wash sale rule"))
        assert result["route"] == "tax_education"
        assert "not tax advice" in result["answer"].lower()
    finally:
        cfg.settings.OPENAI_API_KEY = orig
