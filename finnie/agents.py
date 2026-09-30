"""Six specialist agents behind one chat interface.

Each agent is an async callable taking (query, context) and returning a
markdown string. When OPENAI_API_KEY is set they use the LLM with RAG
grounding; otherwise they degrade to deterministic RAG-based answers so the
app still runs offline.
"""
from __future__ import annotations

import re

from finnie.config import settings
from finnie.rag import kb
from finnie.tools import (
    DEFAULT_PORTFOLIO,
    compound_growth,
    get_quote,
    lump_sum_growth,
    portfolio_summary,
    search_news,
)

TAX_DISCLAIMER = (
    "\n\n> **Educational purposes only — this is not tax advice.** "
    "Tax rules are complex and personal. Consult a licensed tax professional "
    "before acting."
)


def _llm():
    if not settings.llm_available:
        return None
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(model=settings.LLM_MODEL, temperature=0.3)


async def _ask_llm(system: str, user: str) -> str | None:
    llm = _llm()
    if llm is None:
        return None
    import asyncio

    resp = await asyncio.to_thread(
        llm.invoke,
        [{"role": "system", "content": system}, {"role": "user", "content": user}],
    )
    return resp.content


def _rag_block(query: str, k: int = 3) -> str:
    try:
        docs = kb.retrieve(query, k=k)
    except Exception:
        return ""
    if not docs:
        return ""
    parts = [f"### {d['title']}\n{d['text'][:600]}" for d in docs]
    return "\n\n".join(parts)


def _citations(query: str) -> str:
    try:
        docs = kb.retrieve(query, k=3)
    except Exception:
        return ""
    if not docs:
        return ""
    return "\n\n**Sources:** " + ", ".join(f"_{d['title']}_" for d in docs)


# ---------------------------------------------------------------------------
# 1. Finance Q&A
# ---------------------------------------------------------------------------
_LUMP_SUM_SIGNALS = re.compile(
    r"\b(?:one[-\s]?time|once|lump[-\s]?sum|single investment|one[-\s]?off|future value)\b",
    re.IGNORECASE,
)
_MONEY_RE = re.compile(r"\$([\d,]+(?:\.\d+)?)\s*([kKmM]?)\b")
_RATE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:%|percent)")
_YEARS_RE = re.compile(r"(\d+(?:\.\d+)?)\s*years?")


def _parse_lump_sum(query: str) -> tuple[float, float, float] | None:
    """Extract (principal, annual_rate_pct, years) from a one-time
    investment growth question like 'invest $10,000 once at 7% for 10
    years'. Returns None when the query isn't a lump-sum growth question.
    """
    if not _LUMP_SUM_SIGNALS.search(query):
        return None
    m = _MONEY_RE.search(query.replace(",", ""))
    rate = _RATE_RE.search(query)
    years = _YEARS_RE.search(query)
    if not m or rate is None or years is None:
        return None
    principal = float(m.group(1))
    suffix = m.group(2).lower()
    if suffix == "k":
        principal *= 1_000
    elif suffix == "m":
        principal *= 1_000_000
    return principal, float(rate.group(1)), float(years.group(1))


def _lump_sum_answer(query: str) -> str | None:
    """Deterministic FV answer for one-time investment growth questions.

    Computes FV = principal * (1 + r) ** years exactly — this is a lump
    sum, never a monthly-savings plan.
    """
    parsed = _parse_lump_sum(query)
    if parsed is None:
        return None
    principal, rate_pct, years = parsed
    fv = lump_sum_growth(principal, rate_pct, years)
    return "\n".join([
        "# One-Time Investment Growth",
        "",
        f"**${principal:,.2f}** invested once at **{rate_pct:g}%** annual return "
        f"for **{years:g} years** grows to **${fv:,.2f}**.",
        "",
        f"Calculation: ${principal:,.2f} × (1 + {rate_pct:g}%)^({years:g}) "
        f"= ${fv:,.2f}",
        "",
        "Assumptions: annual compounding, return before taxes/fees/inflation. "
        "_Educational estimate only — not financial advice._",
    ])


async def finance_qa(query: str, context: dict) -> str:
    # One-time investment growth is answered deterministically (works
    # offline and with the LLM): never let it fall through to a generic
    # or LLM-guessed response.
    lump = _lump_sum_answer(query)
    if lump:
        return lump
    grounding = _rag_block(query)
    answer = await _ask_llm(
        "You are FINNIE, a friendly finance educator. Answer concisely in "
        "markdown. Ground your answer in the provided knowledge base excerpts. "
        "Never give personalized investment advice; speak in general "
        "educational terms.",
        f"Knowledge base excerpts:\n{grounding}\n\nQuestion: {query}",
    )
    if answer:
        return answer + _citations(query)
    # Offline fallback: synthesize directly from RAG.
    if grounding:
        return (
            "Here's what I found in the knowledge base:\n\n" + grounding
            + _citations(query)
            + "\n\n_(Offline mode — set OPENAI_API_KEY for full answers.)_"
        )
    return "I couldn't find relevant material for that question. Try asking about investing basics, retirement accounts, or risk."


# ---------------------------------------------------------------------------
# 2. Portfolio Analysis
# ---------------------------------------------------------------------------
async def portfolio_agent(query: str, context: dict) -> str:
    positions = context.get("positions") or DEFAULT_PORTFOLIO
    symbols = sorted({p["symbol"].upper() for p in positions})
    quotes, sources = {}, {}
    for s in symbols:
        q = await get_quote(s)
        quotes[s] = q["price"]
        sources[s] = q["source"]
    summary = portfolio_summary(positions, quotes)

    lines = [
        "# Portfolio Analysis",
        f"**Total value:** ${summary['total_value']:,.2f}",
        f"**Total P&L:** ${summary['total_pnl']:,.2f} ({summary['total_pnl_pct']:+.2f}%)",
        "",
        "| Symbol | Shares | Price | Value | Weight | P&L |",
        "|---|---|---|---|---|---|",
    ]
    for r in summary["positions"]:
        lines.append(
            f"| {r['symbol']} | {r['shares']} | ${r['price']:.2f} | "
            f"${r['value']:,.2f} | {r['weight_pct']:.1f}% | "
            f"${r['pnl']:+,.2f} ({r['pnl_pct']:+.1f}%) |"
        )
    mock_note = ""
    if any(src == "mock" for src in sources.values()):
        mock_note = "\n\n_(Quotes are illustrative mock data — add ALPHA_VANTAGE_API_KEY for live prices.)_"

    weights = {r["symbol"]: r["weight_pct"] for r in summary["positions"]}
    top = max(weights, key=weights.get)
    insight = await _ask_llm(
        "You are a portfolio analyst. Given this allocation summary, write 3-5 "
        "concise bullet observations about concentration, diversification, "
        "and risk. Educational only, no personalized advice.",
        f"Query: {query}\nTotal value: ${summary['total_value']:,.2f}, "
        f"P&L {summary['total_pnl_pct']:+.2f}%. Weights: {weights}. "
        f"Largest position: {top}.",
    )
    body = "\n".join(lines)
    if insight:
        body += "\n\n## Observations\n" + insight
    else:
        body += (
            f"\n\n## Observations\n- Largest position: **{top}** "
            f"({weights[top]:.1f}% of portfolio) — watch concentration risk.\n"
            "- Mix of broad ETFs (VOO, QQQ, BND) with single stocks gives "
            "core-satellite structure.\n- BND provides ballast; consider whether "
            "the bond weight matches your time horizon."
        )
    return body + mock_note


# ---------------------------------------------------------------------------
# 3. Market Analysis
# ---------------------------------------------------------------------------
SYMBOL_RE = re.compile(r"\b([A-Z]{2,5})\b")


async def market_agent(query: str, context: dict) -> str:
    # Match tickers in the original casing ("What is the price of AAPL?"
    # -> ["AAPL"]); uppercasing first would match every short word.
    candidates = [s for s in SYMBOL_RE.findall(query) if len(s) >= 2]
    symbols = candidates[:4] or ["SPY", "QQQ"]
    cards = []
    for s in symbols:
        q = await get_quote(s)
        arrow = "▲" if q["change_pct"] >= 0 else "▼"
        cards.append(
            f"- **{q['symbol']}** ({q['name']}): ${q['price']:.2f} "
            f"{arrow} {q['change_pct']:+.2f}%"
        )
    live = (await get_quote(symbols[0]))["source"] == "alpha_vantage"
    note = (
        "\n\n_(Live data via Alpha Vantage.)_"
        if live
        else "\n\n_(Illustrative mock quotes — add ALPHA_VANTAGE_API_KEY for live data.)_"
    )
    commentary = await _ask_llm(
        "You are a market analyst. Given these quotes, write a brief market "
        "read in 3-5 bullets. Educational only; never predict prices or give "
        "buy/sell advice.",
        f"Query: {query}\nQuotes:\n" + "\n".join(cards),
    )
    body = "# Market Snapshot\n" + "\n".join(cards)
    if commentary:
        body += "\n\n## Read\n" + commentary
    return body + note


# ---------------------------------------------------------------------------
# 4. Goal Planning
# ---------------------------------------------------------------------------
GOAL_RE = re.compile(
    r"(?P<target>\$?[\d,]+(?:\.\d+)?)\s*(?P<unit>k|m|million|thousand)?"
    r".{0,40}?(?P<years>\d+)\s*years?", re.IGNORECASE
)


def _parse_goal(query: str) -> tuple[float, int] | None:
    m = GOAL_RE.search(query.replace(",", ""))
    if not m:
        return None
    target = float(m.group("target").lstrip("$"))
    unit = (m.group("unit") or "").lower()
    if unit in ("k", "thousand"):
        target *= 1_000
    elif unit in ("m", "million"):
        target *= 1_000_000
    return target, int(m.group("years"))


async def goals_agent(query: str, context: dict) -> str:
    # Safety net: a one-time investment growth question must get its
    # lump-sum FV answer even if the router ever sends it here.
    lump = _lump_sum_answer(query)
    if lump:
        return lump
    parsed = _parse_goal(query)
    if not parsed:
        return (
            "Tell me your goal in a sentence like: "
            "**'I want $500k in 20 years'** or **'I need $1 million in 15 years'**, "
            "and I'll estimate the monthly savings needed at a few return assumptions."
        )
    target, years = parsed
    rows = []
    for rate in (5.0, 7.0, 9.0):
        r = rate / 100 / 12
        n = years * 12
        monthly = target * r / ((1 + r) ** n - 1) if r > 0 else target / n
        rows.append((rate, monthly))
    lines = [
        f"# Goal Plan: ${target:,.0f} in {years} years",
        "",
        "| Assumed annual return | Monthly savings needed |",
        "|---|---|",
    ]
    for rate, monthly in rows:
        lines.append(f"| {rate:.0f}% | ${monthly:,.2f} |")
    lines += [
        "",
        f"At 7% with ${rows[1][1]:,.2f}/month you'd contribute "
        f"${rows[1][1]*years*12:,.0f} total — compounding does the rest.",
        "",
        "Assumptions: monthly contributions, monthly compounding, returns "
        "before taxes/fees/inflation. _Educational estimate only — not "
        "financial advice._",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 5. News Synthesizer
# ---------------------------------------------------------------------------
async def news_agent(query: str, context: dict) -> str:
    result = await search_news(query, max_results=5)
    items = result["results"]
    src = result["source"]
    bullets = "\n".join(
        f"- **{a['title']}** ({a['source']})\n  {a['snippet']}" for a in items
    )
    synthesis = await _ask_llm(
        "You are a financial news analyst. Synthesize these headlines into a "
        "brief 3-5 bullet market briefing. Stick to what the headlines say; "
        "do not invent facts. Educational only.",
        f"Query: {query}\nHeadlines:\n{bullets}",
    )
    tag = f"\n\n_(News via {src}.)_" if src != "mock" else "\n\n_(Demo headlines — add TAVILY_API_KEY for live news.)_"
    body = "# News Briefing\n" + bullets
    if synthesis:
        body += "\n\n## Synthesis\n" + synthesis
    return body + tag


# ---------------------------------------------------------------------------
# 6. Tax Education (education only — NEVER tax advice)
# ---------------------------------------------------------------------------
async def tax_agent(query: str, context: dict) -> str:
    grounding = _rag_block(query + " tax", k=3)
    answer = await _ask_llm(
        "You are a tax educator. Explain general tax concepts clearly and "
        "concisely in markdown, grounded in the excerpts. You MUST include a "
        "disclaimer that this is educational content, not tax advice, and "
        "that the user should consult a licensed tax professional. Never "
        "recommend specific tax strategies for the user's situation.",
        f"Knowledge base excerpts:\n{grounding}\n\nQuestion: {query}",
    )
    if answer:
        if "not tax advice" not in answer.lower():
            answer += TAX_DISCLAIMER
        return answer + _citations(query + " tax")
    body = "Here's general educational background:\n\n" + grounding if grounding else (
        "I can explain general tax concepts (capital gains, IRAs, "
        "wash-sale rules, RMDs) at an educational level."
    )
    return body + _citations(query + " tax") + TAX_DISCLAIMER


AGENTS = {
    "finance_qa": finance_qa,
    "portfolio": portfolio_agent,
    "market": market_agent,
    "goals": goals_agent,
    "news": news_agent,
    "tax_education": tax_agent,
}

AGENT_DESCRIPTIONS = {
    "finance_qa": "General finance questions, concepts, and how-tos (RAG-grounded).",
    "portfolio": "Portfolio holdings, allocation, and performance analysis.",
    "market": "Live market quotes and market reads for tickers/indexes.",
    "goals": "Goal-based planning: monthly savings needed for a target.",
    "news": "Synthesis of recent financial news and headlines.",
    "tax_education": "General tax education only — never personalized tax advice.",
}
