"""Conversation-context tests — grader feedback rework.

Covers: growth-phrasing routing ("how much will $10k grow at 7%"),
follow-up resolution against prior turns, and portfolio holdings carried
into the graph. All hermetic (offline mode, deterministic classifier).
"""
import asyncio

import finnie.config as cfg
from finnie.agents import _growth_answer, _looks_like_growth_question
from finnie.graph import classify_sync, run_finnie


def _offline():
    orig = cfg.settings.OPENAI_API_KEY
    cfg.settings.OPENAI_API_KEY = None
    return orig


# ---------------------------------------------------------------------------
# Growth-phrasing routing (the grader's explicit example)
# ---------------------------------------------------------------------------

def test_growth_phrasing_routes_to_finance_qa_not_goals():
    q = "how much will $10k grow at 7%"
    assert _looks_like_growth_question(q) is True
    assert classify_sync(q) == "finance_qa"


def test_growth_phrasing_with_years_routes_and_computes():
    q = "how much will $10k grow at 7% for 10 years?"
    assert classify_sync(q) == "finance_qa"
    orig = _offline()
    try:
        result = asyncio.run(run_finnie(q))
        assert result["route"] == "finance_qa"
        # $10,000 x 1.07^10 = $19,671.51
        assert "19,671.51" in result["answer"]
        assert "Monthly savings" not in result["answer"]
    finally:
        cfg.settings.OPENAI_API_KEY = orig


def test_growth_phrasing_without_years_asks_for_horizon():
    # No years -> honest clarifying prompt, never a monthly-savings plan.
    orig = _offline()
    try:
        result = asyncio.run(run_finnie("how much will $10k grow at 7%"))
        assert result["route"] == "finance_qa"
        assert "how many years" in result["answer"].lower()
        assert "Monthly savings" not in result["answer"]
        # The amounts are echoed back so the user sees what was understood.
        assert "10,000" in result["answer"] and "7%" in result["answer"]
    finally:
        cfg.settings.OPENAI_API_KEY = orig


def test_growth_answer_helper_variants():
    assert _growth_answer("how much will $10k grow at 7% for 10 years?") is not None
    assert "19,671.51" in _growth_answer("how much will $10k grow at 7% for 10 years?")
    prompt = _growth_answer("what will $5k grow into at 8%?")
    assert prompt is not None and "how many years" in prompt.lower()
    assert _growth_answer("What is compound interest?") is None


def test_genuine_goals_queries_still_route_to_goals():
    assert classify_sync("I want $1 million in 20 years") == "goals"
    assert classify_sync("How much should I save for retirement?") == "goals"
    assert classify_sync("I want $500k in 15 years, how much per month?") == "goals"


def test_tax_question_with_growth_words_stays_tax():
    # Tax keywords outrank the growth-phrasing check.
    q = "how is tax calculated when my $10k investment grows at 7%?"
    assert classify_sync(q) == "tax_education"


def test_goals_agent_never_emits_savings_plan_for_growth():
    import finnie.agents as agents

    orig = _offline()
    try:
        out = asyncio.run(agents.goals_agent("how much will $10k grow at 7%", {}))
        assert "Monthly savings" not in out
        out2 = asyncio.run(
            agents.goals_agent("how much will $10k grow at 7% for 10 years?", {})
        )
        assert "19,671.51" in out2
        assert "Monthly savings" not in out2
    finally:
        cfg.settings.OPENAI_API_KEY = orig


# ---------------------------------------------------------------------------
# Follow-up resolution against conversation history
# ---------------------------------------------------------------------------

def test_follow_up_resolves_against_prior_turn():
    history = [
        ("user", "If I invest $10,000 once at 7% for 10 years, how much will I have?", "finance_qa"),
    ]
    # "what about $20,000?" alone is ambiguous; with history it stays finance_qa.
    assert classify_sync("what about $20,000?", history) == "finance_qa"


def test_follow_up_without_history_unchanged():
    # No history -> deterministic standalone behavior preserved.
    # ("$" is a goals keyword, so the bare follow-up routes to goals.)
    assert classify_sync("what about $20,000?") == "goals"
    assert classify_sync("What is an ETF?") == "finance_qa"


def test_follow_up_end_to_end_uses_prior_amounts():
    orig = _offline()
    try:
        history = [
            ("user", "invest $10,000 once at 7% for 10 years", "finance_qa"),
        ]
        result = asyncio.run(run_finnie("what about $20,000?", history=history))
        assert result["route"] == "finance_qa"
        # $20,000 x 1.07^10 = $39,343.03 — resolved from the prior turn.
        assert "39,343.03" in result["answer"], result["answer"]
    finally:
        cfg.settings.OPENAI_API_KEY = orig


def test_history_carried_into_agent_context():
    # Agents receive normalized history in context for LLM prompts.
    seen = {}

    async def spy_agent(query, context):
        seen["history"] = context.get("history")
        return "ok"

    import finnie.graph as graph_mod

    orig_agents = graph_mod.AGENTS
    graph_mod.AGENTS = {"finance_qa": spy_agent, **{k: v for k, v in orig_agents.items() if k != "finance_qa"}}
    # Rebuild the cached graph so it picks up the patched AGENTS.
    graph_mod._graph = None
    orig = _offline()
    try:
        history = [("user", "hello", ""), ("assistant", "hi", "finance_qa")]
        asyncio.run(run_finnie("What is an ETF?", history=history))
        assert seen["history"] is not None
        assert seen["history"][0]["role"] == "user"
        assert seen["history"][0]["content"] == "hello"
    finally:
        graph_mod.AGENTS = orig_agents
        graph_mod._graph = None
        cfg.settings.OPENAI_API_KEY = orig


# ---------------------------------------------------------------------------
# Portfolio holdings threaded into the graph
# ---------------------------------------------------------------------------

def test_portfolio_positions_reach_portfolio_agent():
    orig = _offline()
    cfg.settings.ALPHA_VANTAGE_API_KEY = None
    try:
        positions = [{"symbol": "AAPL", "shares": 10, "avg_cost": 100.0}]
        result = asyncio.run(
            run_finnie("Analyze my portfolio", portfolio=positions)
        )
        assert result["route"] == "portfolio"
        # Custom holdings used (not the default 5-position portfolio):
        # 10 x AAPL @ mock $232.40 = $2,324.00 total, single table row.
        assert "| AAPL |" in result["answer"]
        assert "| VOO |" not in result["answer"]
        assert "2,324.00" in result["answer"]
        assert "mock" in result["answer"].lower()  # honest mock labelling kept
    finally:
        cfg.settings.OPENAI_API_KEY = orig
