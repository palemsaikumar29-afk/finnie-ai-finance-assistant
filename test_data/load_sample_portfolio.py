"""Load test_data/sample_portfolio.csv and print a portfolio summary.

Usage:  python test_data/load_sample_portfolio.py
"""
from __future__ import annotations

import asyncio
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from finnie.tools import get_quote, portfolio_summary  # noqa: E402

CSV_PATH = Path(__file__).parent / "sample_portfolio.csv"


async def main() -> None:
    positions = []
    with open(CSV_PATH, newline="") as f:
        for row in csv.DictReader(f):
            positions.append(
                {
                    "symbol": row["ticker"].strip().upper(),
                    "shares": float(row["shares"]),
                    "avg_cost": float(row["buy_price"]),
                }
            )
    quotes = {}
    for p in positions:
        q = await get_quote(p["symbol"])
        quotes[p["symbol"]] = q["price"]
        print(f"{p['symbol']:6s} ${q['price']:8.2f}  (source: {q['source']})")
    s = portfolio_summary(positions, quotes)
    print(f"\nTotal value: ${s['total_value']:,.2f}")
    print(f"Total P&L:   ${s['total_pnl']:+,.2f} ({s['total_pnl_pct']:+.2f}%)")


if __name__ == "__main__":
    asyncio.run(main())
