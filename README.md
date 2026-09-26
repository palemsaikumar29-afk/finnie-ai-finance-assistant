# FINNIE — AI Finance Assistant

Capstone Project 1 · Interview Kickstart · Applied Agentic AI for SWEs

FINNIE is a multi-agent finance assistant. Every query goes through a
**LangGraph router** that classifies it and dispatches to one of **six
specialist agents** behind a single chat interface:

| Agent | Handles |
|---|---|
| `finance_qa` | General finance questions, grounded in a RAG knowledge base |
| `portfolio` | Portfolio holdings, allocation, P&L analysis |
| `market` | Live market quotes + market reads |
| `goals` | Goal planning — monthly savings needed for a target |
| `news` | Financial news synthesis |
| `tax_education` | Tax **education only** — never tax advice (always disclaimed) |

## Setup

```bash
cd capstone-1-finnie
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Generate the knowledge base (67 finance articles) — done once
python -m finnie.knowledge_builder
```

## API keys (environment variables only — never committed)

```bash
export OPENAI_API_KEY="..."        # router + agents (course key)
export TAVILY_API_KEY="..."        # news search (primary)
export SERPAPI_API_KEY="..."       # news search (fallback)
export ALPHA_VANTAGE_API_KEY="..." # live quotes
```

Every tool **degrades to realistic mock data** when its key is missing, so the
app always runs. Alpha Vantage quotes are cached aggressively (30-min TTL;
free tier is 25 requests/day — the "#1 demo killer").

## Run

```bash
streamlit run app.py
```

Tabs: **Chat** (routed multi-agent Q&A) · **Portfolio** (editable holdings +
allocation) · **Markets** (quote lookup) · **Goals** (savings planner) ·
**Knowledge** (RAG search over the article library).

## Tests

```bash
pytest tests/ -q
```

Covers the router classifier (keyword fallback, hermetic), end-to-end routing,
quote mock-fallback + cache TTL, news mock-fallback, and portfolio math.

## Project structure

```
app.py                    Streamlit UI (5 tabs)
finnie/
  __init__.py
  config.py               env-based settings
  graph.py                LangGraph router + dispatch
  agents.py               6 specialist agents
  tools.py                quotes (cached) / news (Tavily→SerpApi→mock) / math
  rag.py                  FAISS + sentence-transformers retrieval
  knowledge_builder.py    generates 67 finance articles
  knowledge/              generated .md articles (+ faiss index, gitignored)
tests/
  test_router.py
  test_tools.py
test_data/
  sample_portfolio.csv     10-holding sample portfolio for the Portfolio tab
  sample_questions.md      copy-paste questions, 3–4 per specialist agent
  expected_behavior.md     what each sample question should return
  load_sample_portfolio.py CLI loader: prints the sample portfolio summary
```

## Notes / limitations

- Tax agent is education-only with mandatory disclaimers; nothing here is
  financial, investment, or tax advice.
- Mock data is clearly labeled in the UI wherever it is used.
- The FAISS index (`finnie/knowledge/index.faiss`) is gitignored and rebuilt
  automatically on first query if missing.
