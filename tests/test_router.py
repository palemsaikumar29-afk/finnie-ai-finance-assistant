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


# Regression: the verified T1 end-user failure — a one-time investment
# growth question was routed to goals and answered with a monthly-savings
# plan. It must route to finance_qa instead.
_LUMP_SUM_Q1 = (
    "What is compound interest? If I invest $10,000 once at 7% annual "
    "return for 10 years, how much will I have?"
)
_LUMP_SUM_Q2 = (
    "Calculate the future value: one-time investment of $10000, 7 percent "
    "annual return, 10 years. Just give me the final dollar amount."
)


def test_classify_sync_lump_sum_routes_to_finance_qa():
    assert classify_sync(_LUMP_SUM_Q1) == "finance_qa"
    assert classify_sync(_LUMP_SUM_Q2) == "finance_qa"
    assert classify_sync("Lump sum of $50,000 at 6% for 20 years") == "finance_qa"
    # Genuine recurring-savings goals still route to goals.
    assert classify_sync("I want $1 million in 20 years") == "goals"
    assert classify_sync("How much should I save for retirement?") == "goals"


def test_lump_sum_fv_answer_contains_correct_amount():
    import finnie.config as cfg

    # Force offline mode so the test is hermetic.
    orig = cfg.settings.OPENAI_API_KEY
    cfg.settings.OPENAI_API_KEY = None
    try:
        for q in (_LUMP_SUM_Q1, _LUMP_SUM_Q2):
            result = asyncio.run(run_finnie(q))
            assert result["route"] == "finance_qa", f"route was {result['route']}"
            # $10,000 x 1.07^10 = $19,671.51
            assert "19,671.51" in result["answer"], result["answer"]
            # Must NOT be a monthly-savings plan.
            assert "Monthly savings" not in result["answer"]
    finally:
        cfg.settings.OPENAI_API_KEY = orig


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
