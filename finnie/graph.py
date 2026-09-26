"""LangGraph router: classifies each query and dispatches to a specialist."""
from __future__ import annotations

import re
from typing import TypedDict

from langgraph.graph import END, StateGraph

from finnie.agents import AGENTS, _ask_llm
from finnie.config import settings


class FinnieState(TypedDict):
    query: str
    route: str
    context: dict
    answer: str


ROUTER_PROMPT = """You are FINNIE's router. Classify the user query into exactly one of:
- finance_qa: general finance concepts, how-tos, definitions
- portfolio: questions about the user's holdings, allocation, performance
- market: stock/ETF prices, ticker quotes, market moves
- goals: savings targets, retirement planning, "how much do I need"
- news: recent headlines, current events, news about a company/market
- tax_education: any question about taxes (answer educationally, never advice)

Reply with ONLY the category name."""


# Keyword fallback when no LLM key is available (also used in tests).
_KEYWORD_ROUTES: list[tuple[str, list[str]]] = [
    ("tax_education", ["tax", "irs", "deduction", "capital gain", "wash sale", "rmd", "1099"]),
    ("news", ["news", "headlines", "latest", "happening", "fed announced", "earnings"]),
    ("portfolio", ["portfolio", "holdings", "allocation", "my stocks", "my positions", "p&l", "pnl"]),
    ("market", ["price of", "quote", "ticker", "stock price", "market", "spy", "qqq", "aapl", "msft", "nvda", "tsla"]),
    ("goals", ["retire", "goal", "save for", "how much", "million", "$", "down payment", "college fund"]),
]


def classify_sync(query: str) -> str:
    q = query.lower()
    for route, keywords in _KEYWORD_ROUTES:
        if any(k in q for k in keywords):
            return route
    return "finance_qa"


async def classify(query: str) -> str:
    """LLM classification with deterministic keyword fallback."""
    if settings.llm_available:
        try:
            label = await _ask_llm(ROUTER_PROMPT, query)
            label = (label or "").strip().lower()
            if label in AGENTS:
                return label
        except Exception:
            pass
    return classify_sync(query)


async def router_node(state: FinnieState) -> FinnieState:
    route = await classify(state["query"])
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


async def run_finnie(query: str, context: dict | None = None) -> dict:
    """Run one query through the router; returns {'route', 'answer'}."""
    graph = get_graph()
    result = await graph.ainvoke(
        {"query": query, "route": "", "context": context or {}, "answer": ""}
    )
    return {"route": result["route"], "answer": result["answer"]}
