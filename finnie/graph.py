"""LangGraph router: classifies each query and dispatches to a specialist."""
from __future__ import annotations

import re
from typing import TypedDict

from langgraph.graph import END, StateGraph

from finnie.agents import AGENTS, _ask_llm, _looks_like_growth_question, _parse_lump_sum
from finnie.config import settings


class FinnieState(TypedDict):
    query: str
    route: str
    context: dict
    history: list
    answer: str


ROUTER_PROMPT = """You are FINNIE's router. Classify the user query into exactly one of:
- finance_qa: general finance concepts, how-tos, definitions, and ONE-TIME
  investment growth calculations (e.g. "invest $10,000 once at 7% for 10
  years — how much will I have?", "future value of a lump sum")
- portfolio: questions about the user's holdings, allocation, performance
- market: stock/ETF prices, ticker quotes, market moves
- goals: savings targets, retirement planning, recurring contributions,
  "how much do I need to SAVE (per month)"
- news: recent headlines, current events, news about a company/market
- tax_education: any question about taxes (answer educationally, never advice)

IMPORTANT: a one-time investment growth question is finance_qa, NEVER goals.
goals is only for questions about saving repeatedly toward a target.

Reply with ONLY the category name.

If the current question is a follow-up (e.g. "what about at 9%?"), use the
conversation history to interpret what it refers to before classifying."""


# Keyword fallback when no LLM key is available (also used in tests).
# goals is checked separately AFTER the growth-phrasing check so that
# "how much will $10k grow at 7%" can't be swallowed by "$"/"how much".
_KEYWORD_ROUTES: list[tuple[str, list[str]]] = [
    ("tax_education", ["tax", "irs", "deduction", "capital gain", "wash sale", "rmd", "1099"]),
    ("news", ["news", "headlines", "latest", "happening", "fed announced", "earnings"]),
    ("portfolio", ["portfolio", "holdings", "allocation", "my stocks", "my positions", "p&l", "pnl"]),
    ("market", ["price of", "quote", "ticker", "stock price", "market", "spy", "qqq", "aapl", "msft", "nvda", "tsla"]),
]
_GOALS_KEYWORDS = ["retire", "goal", "save for", "how much", "million", "$", "down payment", "college fund"]

_FOLLOWUP_OPENERS = re.compile(
    r"^\s*(what about|how about|and if|what if|and at|and for|"
    r"ok[,.]?\s+(what|how) about)\b",
    re.IGNORECASE,
)
_PRONOUN_RE = re.compile(r"\b(it|that|those|them|this)\b", re.IGNORECASE)


def _is_follow_up(query: str) -> bool:
    """Heuristic: is this message a follow-up that needs prior context?"""
    if _FOLLOWUP_OPENERS.search(query):
        return True
    words = query.split()
    return len(words) <= 7 and _PRONOUN_RE.search(query) is not None


def _last_user_message(history: list | None) -> str:
    for turn in reversed(history or []):
        if isinstance(turn, dict):
            if turn.get("role") == "user":
                return turn.get("content", "")
        elif isinstance(turn, (list, tuple)) and len(turn) >= 2 and turn[0] == "user":
            return turn[1]
    return ""


def _normalize_history(history: list | None) -> list:
    """Accept (role, content[, route]) tuples or dicts; keep the last 8."""
    norm = []
    for turn in history or []:
        if isinstance(turn, dict):
            norm.append({
                "role": turn.get("role", ""),
                "content": turn.get("content", ""),
                "route": turn.get("route", ""),
            })
        elif isinstance(turn, (list, tuple)) and len(turn) >= 2:
            norm.append({
                "role": turn[0],
                "content": turn[1],
                "route": turn[2] if len(turn) > 2 else "",
            })
    return norm[-8:]


def _history_snippet(history: list | None) -> str:
    lines = []
    for t in (history or [])[-6:]:
        role = t.get("role", "")
        content = (t.get("content") or "")[:300]
        if role in ("user", "assistant") and content:
            lines.append(f"{role}: {content}")
    return "\n".join(lines)


def resolve_query(query: str, history: list | None) -> str:
    """Resolve a follow-up against the previous user message.

    Returns "<current query> <previous user message>" so that entities
    in the current message take precedence when parsing, while the prior
    turn supplies the missing context. Non-follow-ups pass through
    unchanged.
    """
    if _is_follow_up(query):
        prev = _last_user_message(history)
        if prev:
            return query + " " + prev
    return query


def classify_sync(query: str, history: list | None = None) -> str:
    effective = resolve_query(query, history)
    q = effective.lower()
    # One-time investment growth ("invest $X once at r% for N years") is a
    # finance-QA calculation — check before the keyword rules so the
    # goals entry ("$", "how much") can't swallow it.
    if _parse_lump_sum(effective) is not None:
        return "finance_qa"
    for route, keywords in _KEYWORD_ROUTES:
        if any(k in q for k in keywords):
            return route
    # Growth phrasings ("how much will $10k grow at 7%") are finance-QA,
    # checked before goals keywords for the same reason as above.
    if _looks_like_growth_question(effective):
        return "finance_qa"
    if any(k in q for k in _GOALS_KEYWORDS):
        return "goals"
    return "finance_qa"


async def classify(query: str, history: list | None = None) -> str:
    """LLM classification with deterministic keyword fallback."""
    if settings.llm_available:
        try:
            user_msg = query
            snippet = _history_snippet(history)
            if snippet:
                user_msg = (
                    "Conversation so far:\n" + snippet
                    + "\n\nCurrent question: " + query
                )
            label = await _ask_llm(ROUTER_PROMPT, user_msg)
            label = (label or "").strip().lower()
            if label in AGENTS:
                return label
        except Exception:
            pass
    return classify_sync(query, history)


async def router_node(state: FinnieState) -> FinnieState:
    route = await classify(state["query"], state.get("history"))
    return {**state, "route": route}


def _make_agent_node(name: str):
    async def node(state: FinnieState) -> FinnieState:
        answer = await AGENTS[name](state["query"], state.get("context") or {})
        return {**state, "answer": answer}

    node.__name__ = f"{name}_node"
    return node


def build_graph():
    builder = StateGraph(FinnieState)
    builder.add_node("router", router_node)
    for name in AGENTS:
        builder.add_node(name, _make_agent_node(name))
        builder.add_edge(name, END)
    builder.set_entry_point("router")
    builder.add_conditional_edges(
        "router", lambda s: s["route"], {name: name for name in AGENTS}
    )
    return builder.compile()


_graph = None


def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


async def run_finnie(
    query: str,
    context: dict | None = None,
    history: list | None = None,
    portfolio: list[dict] | None = None,
) -> dict:
    """Run one query through the router; returns {'route', 'answer'}.

    history: recent turns as (role, content[, route]) tuples or dicts —
        carried into routing so follow-ups resolve against prior context.
    portfolio: current holdings [{symbol, shares, avg_cost}] — threaded
        into the portfolio agent's context.
    """
    ctx = dict(context or {})
    if portfolio:
        ctx["positions"] = portfolio
    norm_history = _normalize_history(history)
    if norm_history:
        ctx["history"] = norm_history
    # Resolve follow-ups once so routing AND answering see full intent.
    resolved = resolve_query(query, norm_history)
    graph = get_graph()
    result = await graph.ainvoke(
        {
            "query": resolved,
            "route": "",
            "context": ctx,
            "history": norm_history,
            "answer": "",
        }
    )
    return {"route": result["route"], "answer": result["answer"]}
