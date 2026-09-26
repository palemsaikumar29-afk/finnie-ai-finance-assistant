# FINNIE — Expected Behavior for Sample Questions

What you should see when running the samples in
[`sample_questions.md`](sample_questions.md). "Mock" vs "live" depends on
which API keys are exported (see README) — the app labels every answer.

## Finance Q&A

- Answers grounded in the 67-article knowledge base, with a **Sources** line
  naming the articles used (e.g. _Compound Interest: The Eighth Wonder_).
- With `OPENAI_API_KEY` set: fluent LLM answer citing the articles.
- Without it: "Offline mode" summary assembled directly from the top
  retrieved articles.

## Portfolio Analysis

- Table of positions with price, market value, weight %, and P&L per holding,
  plus total portfolio value and total P&L.
- 3–5 bullet observations (concentration, diversification, risk).
- Prices are **mock data** unless `ALPHA_VANTAGE_API_KEY` is set; the UI says
  which. Quotes are cached for 30 minutes (watch for the `(cached)` label).
- The Portfolio tab's data editor accepts CSV-style edits; to load
  [`sample_portfolio.csv`](sample_portfolio.csv), copy its rows into the
  table editor and press **Analyze portfolio**.

## Market Analysis

- One card per ticker: price, day change %, company/ETF name.
- Short market read in bullets. Never predicts prices or says buy/sell.
- Mock vs live labeled per quote.

## Goal Planning

- A table like:

  | Assumed annual return | Monthly savings needed |
  |---|---|
  | 5% | $… |
  | 7% | $… |
  | 9% | $… |

- For "$1 million in 20 years" at 7%, expect roughly **$1,973/month**.
- Includes the assumptions footnote (monthly compounding, before
  taxes/fees/inflation; educational estimate only).
- If the goal can't be parsed, the agent asks for the
  "I want $X in Y years" format instead of guessing.

## News Synthesizer

- Headline list (title, source, snippet) + a short synthesis in bullets.
- With `TAVILY_API_KEY`: real headlines labeled "News via tavily".
- With only `SERPAPI_API_KEY`: "News via serpapi".
- With neither: clearly-labeled demo headlines.

## Tax Education

- General educational explanation with a **Sources** line.
- **Always** ends with a disclaimer: educational purposes only, not tax
  advice, consult a licensed tax professional.
- Never recommends a specific strategy for the user's situation.

## Sample portfolio CSV

[`sample_portfolio.csv`](sample_portfolio.csv) holds 10 realistic holdings
(ticker, shares, buy_price). Run
`python test_data/load_sample_portfolio.py` — with mock quotes expect a
total value near **$71.8k** and P&L near **+$5.0k (+7.5%)** (buy prices are
set below the mock quote prices). Note: the Chat tab's built-in demo
portfolio is a different, smaller 4-position portfolio (~$51.3k with mock
quotes). Exact numbers move with the mock price table in
`finnie/tools.py`.
