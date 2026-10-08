"""FINNIE — AI Finance Assistant. Streamlit UI.

Tabs: Chat | Portfolio | Markets | Goals | Knowledge

Run:  streamlit run app.py
Keys via environment: OPENAI_API_KEY, TAVILY_API_KEY, SERPAPI_API_KEY,
ALPHA_VANTAGE_API_KEY (all optional — the app degrades to mock data).
"""
from __future__ import annotations

import asyncio

import streamlit as st

from finnie.agents import AGENT_DESCRIPTIONS
from finnie.config import settings
from finnie.graph import run_finnie
from finnie.rag import kb
from finnie.tools import DEFAULT_PORTFOLIO, compound_growth, get_quote, search_news

st.set_page_config(page_title="FINNIE — AI Finance Assistant", page_icon="💰", layout="wide")
st.title("💰 FINNIE — AI Finance Assistant")
st.caption(
    "Six specialist agents behind one chat: Finance Q&A · Portfolio · Markets · "
    "Goals · News · Tax Education"
)

with st.sidebar:
    st.header("Status")
    st.write("🤖 LLM:", "✅" if settings.llm_available else "⚠️ offline mode")
    st.write("📰 News:", "✅ live" if settings.news_search_available else "⚠️ demo headlines")
    st.write("📈 Quotes:", "✅ live" if settings.live_quotes_available else "⚠️ mock data")
    st.divider()
    st.header("Agents")
    for name, desc in AGENT_DESCRIPTIONS.items():
        st.write(f"**{name}** — {desc}")
    st.divider()
    st.caption("Educational tool — not financial, investment, or tax advice.")


def _run(coro):
    return asyncio.run(coro)


def _as_position_dicts(rows) -> list[dict]:
    """Normalize Portfolio-tab editor output (DataFrame or list of dicts)
    into [{symbol, shares, avg_cost}] for the chat graph context."""
    if rows is None:
        return []
    if hasattr(rows, "to_dict"):  # pandas DataFrame from st.data_editor
        rows = rows.to_dict("records")
    out = []
    for p in rows or []:
        try:
            sym = str(p.get("symbol", "")).strip().upper()
            if not sym or sym == "NAN":
                continue
            out.append({
                "symbol": sym,
                "shares": float(p.get("shares") or 0),
                "avg_cost": float(p.get("avg_cost") or 0),
            })
        except (AttributeError, TypeError, ValueError):
            continue
    return out


tab_chat, tab_portfolio, tab_markets, tab_goals, tab_knowledge = st.tabs(
    ["💬 Chat", "📊 Portfolio", "📈 Markets", "🎯 Goals", "📚 Knowledge"]
)

# ---------------------------------------------------------------- Chat
with tab_chat:
    if "history" not in st.session_state:
        st.session_state.history = []
    for role, text, route in st.session_state.history:
        with st.chat_message(role):
            if route:
                st.caption(f"routed to `{route}`")
            st.markdown(text)
    prompt = st.chat_input("Ask about investing, markets, your portfolio, goals, news, taxes…")
    if prompt:
        st.session_state.history.append(("user", prompt, ""))
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Routing to specialist…"):
                result = _run(
                    run_finnie(
                        prompt,
                        history=st.session_state.history,
                        portfolio=st.session_state.get("finnie_positions"),
                    )
                )
            st.caption(f"routed to `{result['route']}`")
            st.markdown(result["answer"])
        st.session_state.history.append(("assistant", result["answer"], result["route"]))

# ---------------------------------------------------------- Portfolio
with tab_portfolio:
    st.header("Portfolio Overview")
    positions = list(DEFAULT_PORTFOLIO)
    edited = st.data_editor(
        [{"symbol": p["symbol"], "shares": p["shares"], "avg_cost": p["avg_cost"]} for p in positions],
        num_rows="dynamic",
        key="positions",
    )
    # Keep the edited holdings in session state so the Chat tab can pass
    # them into the graph; also fixes data_editor returning a DataFrame.
    st.session_state["finnie_positions"] = _as_position_dicts(edited)
    if st.button("Analyze portfolio"):
        with st.spinner("Fetching quotes…"):
            normed = st.session_state["finnie_positions"] or _as_position_dicts(DEFAULT_PORTFOLIO)
            quotes = {s: (_run(get_quote(s)))["price"] for s in {p["symbol"] for p in normed}}
        from finnie.tools import portfolio_summary

        summary = portfolio_summary(normed, quotes)
        c1, c2, c3 = st.columns(3)
        c1.metric("Total value", f"${summary['total_value']:,.2f}")
        c2.metric("Total P&L", f"${summary['total_pnl']:+,.2f}", f"{summary['total_pnl_pct']:+.2f}%")
        c3.metric("Positions", len(summary["positions"]))
        st.dataframe(summary["positions"], use_container_width=True)
        st.bar_chart(
            {r["symbol"]: r["weight_pct"] for r in summary["positions"]},
            use_container_width=True,
        )

# ------------------------------------------------------------- Markets
with tab_markets:
    st.header("Market Quotes")
    symbols = st.text_input("Tickers (comma-separated)", "SPY, QQQ, AAPL, MSFT, NVDA")
    if st.button("Get quotes"):
        for sym in [s.strip().upper() for s in symbols.split(",") if s.strip()]:
            with st.spinner(f"Fetching {sym}…"):
                q = _run(get_quote(sym))
            delta = f"{q['change_pct']:+.2f}%"
            src = "live" if q["source"] == "alpha_vantage" else "mock"
            cached = " (cached)" if q.get("cached") else ""
            st.metric(f"{q['symbol']} — {q['name']}", f"${q['price']:.2f}", delta)
            st.caption(f"source: {src}{cached}")

# --------------------------------------------------------------- Goals
with tab_goals:
    st.header("Goal Planner")
    goal_name = st.text_input("Goal name", "Retirement nest egg")
    target = st.number_input("Target amount ($)", min_value=1_000, value=1_000_000, step=10_000)
    years = st.slider("Years", 1, 40, 20)
    if st.button("Calculate plan"):
        st.subheader(goal_name)
        for rate in (5.0, 7.0, 9.0):
            monthly = target * (rate / 100 / 12) / ((1 + rate / 100 / 12) ** (years * 12) - 1)
            total_in = monthly * years * 12
            st.write(
                f"**{rate:.0f}% return** → save **\\${monthly:,.2f}/month** "
                f"(\\${total_in:,.0f} contributions; compounding covers the rest)"
            )
        st.caption("Monthly compounding, before taxes/fees/inflation. Educational estimate only.")
        proj = compound_growth(500, 7.0, years)
        st.info(f"For reference: \\$500/month at 7% for {years} years → \\${proj:,.0f}.")

# ------------------------------------------------------------ Knowledge
with tab_knowledge:
    st.header("Knowledge Base Search")
    st.caption("Grounded in FINNIE's finance article library (FAISS + embeddings).")
    q = st.text_input("Search the knowledge base", "What is dollar-cost averaging?")
    if st.button("Search") and q:
        with st.spinner("Searching…"):
            docs = _run(kb.aretrieve(q, k=5))
        for d in docs:
            with st.expander(f"{d['title']} (score {d['score']:.3f})"):
                st.markdown(d["text"][:1500])
