"""Generates the FINNIE knowledge base: 50+ short finance articles as .md files.

Run:  python -m finnie.knowledge_builder
"""
from __future__ import annotations

from pathlib import Path

KB_DIR = Path(__file__).parent / "knowledge"

ARTICLES: list[tuple[str, str, str]] = [
    # (slug, title, body)
    (
        "compound-interest",
        "Compound Interest: The Eighth Wonder",
        "Compound interest means you earn returns not only on your original "
        "investment but also on the returns it has already generated. Over "
        "long periods this snowball effect dominates: $10,000 invested at 7% "
        "annual return grows to roughly $19,672 in 10 years, $38,697 in 20 "
        "years, and $76,123 in 30 years. Time is the biggest lever — starting "
        "ten years earlier can matter more than saving a slightly larger "
        "amount later. Compounding works for you in investing and against you "
        "in debt (credit card balances compound the same way). Key takeaway: "
        "start early, contribute consistently, reinvest dividends, and keep "
        "fees low so more of the compounding stays in your pocket.",
    ),
    (
        "rule-of-72",
        "The Rule of 72: Doubling Your Money",
        "The Rule of 72 is a quick mental shortcut: divide 72 by your annual "
        "rate of return to estimate how many years it takes money to double. "
        "At 7%, money doubles in about 10.3 years; at 10%, about 7.2 years; "
        "at 3% (a savings account), about 24 years. It also works in reverse "
        "for inflation: at 3% inflation, prices double roughly every 24 years, "
        "halving your purchasing power. The rule is an approximation (most "
        "accurate for rates between 6% and 10%) but it is invaluable for "
        "sanity-checking any return claim — if someone promises 20% annual "
        "returns, the rule says they claim to double your money every 3.6 "
        "years, which should invite serious skepticism.",
    ),
    (
        "etf-vs-mutual-funds",
        "ETFs vs Mutual Funds",
        "Exchange-traded funds (ETFs) and mutual funds both pool investor "
        "money to buy diversified portfolios, but differ in trading, pricing, "
        "and taxes. ETFs trade on exchanges all day at market prices like "
        "stocks; mutual funds price once daily after market close. ETFs are "
        "generally more tax-efficient because their creation/redemption "
        "mechanism avoids distributing capital gains to shareholders the way "
        "mutual funds do. Index ETFs typically charge 0.03%-0.20% annually, "
        "far below many actively managed mutual funds at 0.50%-1.50%. Mutual "
        "funds may still suit investors who prefer automatic investing with "
        "fractional dollars or whose 401(k) offers only mutual funds. For most "
        "long-term investors, low-cost index ETFs are the default choice.",
    ),
    (
        "index-funds",
        "Index Funds Explained",
        "An index fund is a fund that tracks a market index such as the S&P "
        "500 instead of trying to beat it. Because the strategy is passive — "
        "just owning the index's constituents in the right weights — costs "
        "are minimal: flagship S&P 500 index funds charge around 0.03% per "
        "year. Decades of data show most active managers underperform their "
        "benchmark after fees over 10-15 year horizons. Index funds give you "
        "instant diversification across hundreds of companies, transparent "
        "holdings, and low turnover (which also means fewer taxable "
        "distributions). Criticisms include concentration risk when a few "
        "mega-cap stocks dominate an index, but for core equity exposure, "
        "broad-market index funds remain the evidence-based default.",
    ),
    (
        "401k-basics",
        "401(k) Basics",
        "A 401(k) is an employer-sponsored retirement account. Contributions "
        "are made from your paycheck, often with an employer match — e.g., "
        "50% of contributions up to 6% of salary, which is effectively free "
        "money you should capture first. In 2026 the employee contribution "
        "limit is $24,500 ($31,500 if 50+). Traditional 401(k) contributions "
        "are pre-tax (you pay tax on withdrawal in retirement); Roth 401(k) "
        "contributions are after-tax (qualified withdrawals are tax-free). "
        "Money grows tax-deferred either way. Investments are chosen from "
        "your plan's menu — target-date funds are a reasonable default. "
        "Withdrawals before age 59½ generally incur a 10% penalty plus taxes, "
        "so treat this as long-term money.",
    ),
    (
        "traditional-vs-roth-ira",
        "Traditional vs Roth IRA",
        "IRAs let individuals save for retirement outside an employer plan, "
        "with a 2026 contribution limit of $7,500 ($8,500 if 50+). A "
        "traditional IRA may give you a tax deduction now; you pay ordinary "
        "income tax on withdrawals in retirement. A Roth IRA gives no "
        "deduction now, but qualified withdrawals (account open 5+ years and "
        "age 59½+) are completely tax-free. Rough rule: choose Roth if you "
        "expect to be in a higher tax bracket in retirement than today "
        "(common for young earners); choose traditional if you expect a lower "
        "bracket later. High earners may be phased out of Roth contributions "
        "and use the 'backdoor Roth' strategy. This is educational content, "
        "not tax advice — confirm with a tax professional.",
    ),
    (
        "roth-ira-rules",
        "Roth IRA Rules and Withdrawals",
        "Roth IRAs have unique flexibility: you can always withdraw your "
        "contributions (not earnings) tax- and penalty-free at any time, "
        "because you already paid tax on them. Earnings can be withdrawn "
        "tax-free only as a 'qualified distribution' — the account must be "
        "open at least 5 years and you must be 59½, disabled, or using up to "
        "$10,000 for a first home. Non-qualified earnings withdrawals face "
        "income tax plus a 10% early-withdrawal penalty, with exceptions for "
        "hardships like medical expenses. Unlike traditional IRAs, Roth IRAs "
        "have no required minimum distributions for the original owner. "
        "Income limits phase out direct Roth contributions for high earners. "
        "Educational content only — not tax advice.",
    ),
    (
        "diversification",
        "Diversification: Don't Put All Eggs in One Basket",
        "Diversification means spreading investments across assets that don't "
        "move in lockstep, so a single failure can't sink your portfolio. A "
        "portfolio of 20-30 uncorrelated stocks eliminates most company-"
        "specific (unsystematic) risk; what remains is market (systematic) "
        "risk, which diversification can't remove. True diversification spans "
        "dimensions: asset classes (stocks, bonds), geographies (US and "
        "international), sectors, and company sizes. Warning signs of fake "
        "diversification: owning five large-cap US tech funds, or holding "
        "stock in the same company that employs you. A single total-world "
        "stock index fund is already diversified for most investors.",
    ),
    (
        "asset-allocation",
        "Asset Allocation: Your Most Important Decision",
        "Asset allocation — how you split money between stocks, bonds, and "
        "cash — explains the majority of a portfolio's long-term return "
        "differences. Stocks offer higher expected returns with higher "
        "volatility; bonds dampen volatility but drag on long-term growth. A "
        "common starting framework: subtract your age from 110-120 to get a "
        "rough stock percentage, then adjust for your risk tolerance and "
        "time horizon. Money needed within 3-5 years shouldn't be heavily in "
        "stocks. Allocation should reflect goals, not market forecasts — "
        "chasing last year's winner is how investors buy high and sell low. "
        "Revisit your allocation annually or after major life changes.",
    ),
    (
        "rebalancing",
        "Rebalancing Your Portfolio",
        "Over time, winners grow and your allocation drifts — a 80/20 "
        "stock/bond portfolio can become 90/10 after a bull run, silently "
        "raising your risk. Rebalancing sells some winners and buys laggards "
        "to restore your target mix. Two common methods: calendar rebalancing "
        "(e.g., annually) and threshold rebalancing (when any asset drifts "
        "5%+ from target). Rebalancing is contrarian by design — it forces "
        "you to sell high and buy low — and studies show it mainly controls "
        "risk rather than boosting returns. In taxable accounts, prefer "
        "rebalancing with new contributions to avoid triggering capital gains "
        "taxes. Educational content only.",
    ),
    (
        "risk-tolerance",
        "Risk Tolerance vs Risk Capacity",
        "Risk tolerance is psychological — how much volatility you can stomach "
        "without panic-selling. Risk capacity is financial — how much loss you "
        "can afford given your time horizon and obligations. A 25-year-old "
        "with stable income has high capacity even if their tolerance is "
        "shaky; a retiree drawing income has low capacity regardless of "
        "nerves. The 2008 and 2020 crashes showed many investors "
        "overestimated their tolerance. Gauge yours honestly: if a 30% "
        "portfolio drop would make you sell everything, your equity "
        "allocation is too high. The best portfolio is the one you can hold "
        "through a crisis — capacity sets the ceiling, tolerance sets the "
        "floor.",
    ),
    (
        "emergency-fund",
        "Emergency Funds Come Before Investing",
        "An emergency fund is 3-6 months of essential expenses in a safe, "
        "liquid account (high-yield savings), not invested in the market. "
        "Its job is to prevent forced selling of investments — or high-"
        "interest debt — when job loss, medical bills, or car repairs hit. "
        "Freelancers and single-income households should lean toward 6+ "
        "months. Build it before aggressive investing: earning 8% in the "
        "market means little if a $3,000 emergency forces you onto a 24% APR "
        "credit card. Once funded, redirect that monthly amount to investing. "
        "Keep it boring and separate from spending money so it is there when "
        "you need it.",
    ),
    (
        "dollar-cost-averaging",
        "Dollar-Cost Averaging",
        "Dollar-cost averaging (DCA) means investing a fixed amount on a "
        "regular schedule — e.g., $500 every month — regardless of market "
        "levels. You automatically buy more shares when prices are low and "
        "fewer when high, which smooths your average cost and removes the "
        "need to time the market. It is psychologically powerful for nervous "
        "investors and is exactly what 401(k) payroll contributions do. "
        "Caveat: studies show lump-sum investing beats DCA about two-thirds "
        "of the time in rising markets, because markets trend up. DCA's real "
        "value is behavioral — it gets hesitant investors into the market and "
        "keeps them contributing through downturns.",
    ),
    (
        "expense-ratios",
        "Expense Ratios: The Fee That Compounds Against You",
        "An expense ratio is the annual percentage a fund charges on assets — "
        "0.03% on a $100,000 portfolio costs $30/year; 1.00% costs $1,000/"
        "year. The gap compounds brutally: over 30 years at 7% gross returns, "
        "a 1% fee consumes roughly 25-30% of your potential wealth versus a "
        "0.03% fund. Fees are the most reliable predictor of fund "
        "performance — low-cost funds beat high-cost peers far more "
        "consistently than past returns predict future winners. Always check "
        "the expense ratio before buying any fund, and beware of 12b-1 "
        "marketing fees and front-end loads layered on top.",
    ),
    (
        "stocks-basics",
        "Stocks Basics",
        "A stock is a slice of ownership in a company. Shareholders profit two "
        "ways: price appreciation and dividends. Stock prices reflect the "
        "market's collective expectation of future earnings, so they move on "
        "earnings reports, economic data, interest rates, and sentiment. "
        "Common stock typically carries voting rights; preferred stock has "
        "priority on dividends but usually no vote. Individual stocks carry "
        "company-specific risk — a single scandal or disruption can halve a "
        "price — which is why most investors own stocks through diversified "
        "funds. Expected long-term returns for broad equities are around "
        "7-10% nominal annually, with gut-wrenching drawdowns along the way.",
    ),
    (
        "bonds-basics",
        "Bonds Basics",
        "A bond is a loan you make to a government or corporation: you lend "
        "principal, they pay periodic interest (coupons), and return principal "
        "at maturity. Bonds are generally less volatile than stocks and serve "
        "as portfolio ballast. Key risks: interest-rate risk (when rates "
        "rise, existing bond prices fall), credit risk (the issuer may "
        "default), and inflation risk (fixed payments lose purchasing power). "
        "Bond prices and yields move inversely - a fundamental relationship "
        "every investor should internalize. Most individuals own bonds "
        "through total-bond-market funds rather than individual issues.",
    ),
    (
        "bond-duration",
        "Bond Duration and Interest-Rate Sensitivity",
        "Duration measures a bond's price sensitivity to interest-rate "
        "changes, expressed in years. A bond with 5-year duration falls "
        "roughly 5% if rates rise 1%, and rises 5% if rates fall 1%. Longer "
        "maturities and lower coupons mean higher duration and more "
        "sensitivity. This is why long-term bond funds swung wildly in "
        "2022 when rates spiked. Short-duration bonds and cash equivalents "
        "are calmer but yield less. Match duration to your time horizon: "
        "money needed soon belongs in short-duration holdings.",
    ),
    (
        "treasury-bonds",
        "Treasury Securities: T-Bills, Notes, and Bonds",
        "U.S. Treasury securities are backed by the federal government and "
        "considered the global risk-free benchmark. T-bills mature in under "
        "a year and are sold at a discount; T-notes run 2-10 years; T-bonds "
        "run 20-30 years. Interest is exempt from state and local income "
        "tax (but not federal). TIPS (Treasury Inflation-Protected "
        "Securities) adjust principal with CPI, protecting purchasing power. "
        "I Bonds combine a fixed rate with an inflation adjustment and are "
        "popular hedges, though annual purchase limits apply. Educational "
        "content only.",
    ),
    (
        "corporate-bonds",
        "Corporate Bonds and Credit Ratings",
        "Corporate bonds pay higher yields than Treasuries to compensate for "
        "default risk. Credit agencies (Moody's, S&P, Fitch) rate issuers "
        "from AAA down to junk (below BBB-/Baa3). Investment-grade bonds "
        "default rarely; high-yield ('junk') bonds pay more but behave "
        "somewhat like stocks in crises, falling exactly when you want "
        "bonds to stabilize you. Bond funds blend hundreds of issues, "
        "diversifying away single-issuer risk. Watch the fund's average "
        "credit quality and duration - two high-yield funds can behave very "
        "differently from a Treasury fund despite all being called 'bond "
        "funds'.",
    ),
    (
        "yield-curve",
        "The Yield Curve",
        "The yield curve plots bond yields against maturities. Normally it "
        "slopes upward - investors demand more yield for locking money up "
        "longer. An inverted curve (short-term yields above long-term) has "
        "preceded most U.S. recessions, because it signals markets expect "
        "rate cuts ahead. The 2-year/10-year Treasury spread is the most "
        "watched gauge. Inversion doesn't time the downturn precisely - "
        "recessions have followed 6-24 months later - but it is one of the "
        "most reliable macro warning lights in finance.",
    ),
    (
        "dividends",
        "Dividends Explained",
        "Dividends are cash distributions companies pay shareholders from "
        "profits, usually quarterly. Mature, cash-generative firms (utilities, "
        "consumer staples) pay them; fast-growing firms often reinvest "
        "instead. A dividend is not free money - the stock price drops by "
        "roughly the dividend amount on the ex-dividend date. What matters is "
        "total return (price change + dividends). Dividend aristocrats - "
        "companies raising payouts 25+ consecutive years - signal durable "
        "businesses, but chasing the highest yields often leads to troubled "
        "companies about to cut. Reinvesting dividends is a major driver of "
        "long-term compounding.",
    ),
    (
        "dividend-yield",
        "Dividend Yield and Payout Ratio",
        "Dividend yield = annual dividends per share divided by share price. "
        "A 4% yield on a $100 stock pays $4/year. Yields rise when prices "
        "fall, so a soaring yield can signal distress, not bargains. The "
        "payout ratio (dividends divided by earnings) shows sustainability: "
        "30-60% is typically healthy; above 80-100% leaves no cushion and "
        "cuts may follow. Compare yields within sectors, not across - "
        "utilities naturally yield more than tech. For income investors, "
        "dividend growth (rising payouts over time) often beats a high but "
        "stagnant starting yield.",
    ),
    (
        "market-cap",
        "Market Capitalization",
        "Market cap = share price times shares outstanding - the market's "
        "price tag on a company. Rough bands: mega-cap ($200B+), large-cap "
        "($10B-$200B), mid-cap ($2B-$10B), small-cap ($300M-$2B), micro-cap "
        "below that. Large caps are typically stable and liquid; small caps "
        "have historically offered higher long-term returns with sharper "
        "drawdowns. Capitalization-weighted indexes like the S&P 500 "
        "automatically give more weight to bigger companies, so a handful of "
        "mega-caps can dominate index performance.",
    ),
    (
        "pe-ratio",
        "P/E Ratio: Price to Earnings",
        "The price-to-earnings ratio = share price divided by earnings per "
        "share. A P/E of 20 means investors pay $20 for each $1 of annual "
        "earnings. High P/E implies high growth expectations; low P/E can "
        "mean a bargain or a dying business. Trailing P/E uses past "
        "earnings, forward P/E uses estimates. The Shiller CAPE smooths "
        "earnings over 10 inflation-adjusted years to judge whole-market "
        "valuation - readings above ~30 have historically preceded muted "
        "decade-ahead returns. Never use P/E alone: compare within "
        "industries and alongside growth rates and debt levels.",
    ),
    (
        "value-vs-growth",
        "Value vs Growth Investing",
        "Value investors buy stocks that look cheap relative to fundamentals "
        "(low P/E, low price-to-book); growth investors buy fast-expanding "
        "companies at premium prices. Value has outperformed over very long "
        "horizons, but growth can dominate for a decade (as in the 2010s "
        "tech run). The styles are cyclical and unpredictable in timing. "
        "Most index investors own both automatically. Factor purists tilt "
        "toward value for the historical premium; pragmatists hold the "
        "total market and skip the debate. Either way, avoid "
        "performance-chasing between styles based on recent returns.",
    ),
    (
        "large-cap-vs-small-cap",
        "Large-Cap vs Small-Cap Stocks",
        "Large-cap stocks (established giants) offer stability, liquidity, "
        "and dividends; small-caps offer higher growth potential with "
        "greater volatility and deeper drawdowns. Historically small-caps "
        "outperformed over multi-decade stretches, but the premium has been "
        "inconsistent since the 1980s and small-caps lagged large-caps for "
        "much of the 2010s-2020s. A total-market index fund owns both in "
        "market weights - the simplest way to capture whichever segment "
        "leads next without betting on the cycle.",
    ),
    (
        "international-diversification",
        "International Diversification",
        "The U.S. is roughly 60% of global market cap - leaving 40% abroad. "
        "International stocks diversify economic and currency exposure, and "
        "leadership rotates: non-U.S. markets outperformed in the 2000s "
        "while the U.S. dominated the 2010s. Home-country bias (overweighting "
        "your own market) feels comfortable but concentrates risk. A common "
        "approach: hold 20-40% of equities in international index funds. "
        "Currency moves add volatility short-term but wash out over decades. "
        "Emerging markets add growth potential with extra political and "
        "currency risk - size them modestly.",
    ),
    (
        "reits",
        "REITs: Real Estate Investment Trusts",
        "REITs are companies that own income-producing real estate and must "
        "distribute at least 90% of taxable income as dividends, producing "
        "high yields. They trade like stocks, giving liquid exposure to "
        "property sectors - apartments, warehouses, data centers, healthcare. "
        "REIT dividends are mostly taxed as ordinary income (not qualified "
        "dividends), so they are often better held in tax-advantaged "
        "accounts. REITs diversify equity portfolios modestly but crashed "
        "with stocks in 2008 - they are not bond substitutes. Educational "
        "content only.",
    ),
    (
        "inflation",
        "Inflation: The Silent Tax",
        "Inflation erodes purchasing power - 3% annual inflation halves your "
        "money's buying power in about 24 years. It is measured by indexes "
        "like CPI. Moderate inflation is normal; high inflation punishes "
        "cash, fixed-rate bonds, and long-duration assets, while equities, "
        "real estate, and inflation-linked bonds (TIPS, I Bonds) have "
        "historically coped better. When planning, use real (inflation-"
        "adjusted) returns: 7% nominal minus 3% inflation is about 4% real. "
        "Nominal gains that trail inflation are losses in disguise - always "
        "judge returns after inflation.",
    ),
    (
        "real-vs-nominal-returns",
        "Real vs Nominal Returns",
        "Nominal return is the headline number; real return subtracts "
        "inflation - what your money can actually buy. A 6% nominal gain "
        "with 4% inflation is only ~2% real. Taxes take another bite, so "
        "after-tax real return is the truest measure of progress. This "
        "distinction matters most in goal planning: a '7% return' assumption "
        "for retirement math should be real or explicitly nominal with "
        "inflation modeled separately. During high-inflation years, "
        "portfolios can post positive nominal returns while losing "
        "purchasing power.",
    ),
    (
        "target-date-funds",
        "Target-Date Funds: Set-and-Forget Retirement",
        "Target-date funds pick a year near your retirement and automatically "
        "glide from aggressive (mostly stocks) to conservative (more bonds) "
        "as the date approaches. They are the default in many 401(k) plans "
        "for good reason: one fund handles diversification and rebalancing. "
        "Check the expense ratio (index-based ones cost ~0.05-0.15%; "
        "active versions can exceed 0.60%), the glide path's landing point "
        "(some keep gliding past retirement, others stop), and whether the "
        "date matches your actual horizon. One-fund simplicity beats a "
        "neglected hand-built portfolio for most busy savers.",
    ),
    (
        "retirement-withdrawal-4pct",
        "The 4% Rule for Retirement Withdrawals",
        "The 4% rule (from the 1994 Bengen study) suggests withdrawing 4% of "
        "your portfolio in year one of retirement, then adjusting for "
        "inflation annually, giving ~30 years of spending with high "
        "historical success odds. It's a planning rule of thumb, not a law: "
        "low bond yields and long retirements argue for 3-3.5% for extra "
        "safety; flexible strategies (cutting spending after down years) "
        "stretch money further. Sequence-of-returns risk - big losses early "
        "in retirement - is the real danger the rule guards against. Use it "
        "to size your target nest egg (25x annual spending), then refine "
        "with professional planning.",
    ),
    (
        "social-security-basics",
        "Social Security Basics (Educational Overview)",
        "Social Security replaces roughly 40% of pre-retirement earnings for "
        "average earners. You can claim at 62 (reduced ~30%), at full "
        "retirement age 66-67 (100%), or delay to 70 (about 124% via 8%/year "
        "delayed credits). Breakeven math favors delaying if you expect "
        "longevity; health or income needs favor earlier. Benefits are based "
        "on your 35 highest-earning years. Up to 85% of benefits can be "
        "federally taxable depending on income. Spousal and survivor "
        "benefits add planning dimensions for couples. Treat it as a floor "
        "of retirement income, not the whole plan. Educational content only.",
    ),
    (
        "backdoor-roth",
        "Backdoor Roth IRA (Educational Overview)",
        "High earners phased out of direct Roth IRA contributions can use the "
        "'backdoor': contribute after-tax dollars to a traditional IRA, then "
        "convert to Roth. Since the contribution was after-tax, the "
        "conversion is mostly tax-free - except the pro-rata rule, which "
        "taxes the conversion proportionally if you hold other pre-tax IRA "
        "balances. The cleanest setup: roll pre-tax IRA money into a 401(k) "
        "first, leaving only the after-tax contribution to convert. Congress "
        "has periodically threatened to close this, so verify current law. "
        "Educational content only - not tax advice; the pro-rata math is "
        "easy to get wrong.",
    ),
    (
        "net-investment-income-tax",
        "Net Investment Income Tax (Educational Overview)",
        "High earners face an extra 3.8% federal tax on net investment "
        "income (interest, dividends, capital gains, rental income) above "
        "thresholds ($200k single / $250k married filing jointly). It stacks "
        "on top of capital-gains rates, pushing top long-term rates toward "
        "23.8%. It doesn't apply to retirement-account distributions, "
        "municipal bond interest, or active business income. Planning "
        "levers: harvesting gains in lower-income years, Roth conversions "
        "in low-income windows, and muni bonds for taxable accounts. "
        "Educational content only - not tax advice.",
    ),
    (
        "required-minimum-distributions",
        "Required Minimum Distributions (Educational Overview)",
        "The IRS forces withdrawals from traditional 401(k)s and IRAs "
        "starting at age 73 (75 for those born 1960+, under current law) - "
        "required minimum distributions. RMDs are taxed as ordinary income "
        "and calculated from prior-year-end balances divided by life-"
        "expectancy factors. Missing an RMD triggers a steep excise tax "
        "(25%, down from 50%). Strategies to manage the tax torpedo: Roth "
        "conversions in your 60s before RMDs begin, and qualified charitable "
        "distributions (QCDs) directly to charities, which satisfy RMDs "
        "without taxable income. Roth IRAs have no lifetime RMDs for owners. "
        "Educational content only.",
    ),
    (
        "brokerage-vs-retirement-accounts",
        "Brokerage vs Retirement Accounts",
        "Taxable brokerage accounts offer total flexibility - withdraw "
        "anytime, no penalties - but you owe tax yearly on dividends and "
        "realized gains. Retirement accounts (401(k), IRA) give tax "
        "deductions or tax-free growth but lock money up until 59.5 with "
        "penalties for early raids. Funding order for most: 401(k) to the "
        "employer match, then HSA if eligible, then IRA, then max 401(k), "
        "then taxable brokerage. Asset location matters too: hold "
        "tax-inefficient assets (bonds, REITs) in tax-advantaged accounts "
        "and tax-efficient index equities in taxable ones. Educational "
        "content only.",
    ),
    (
        "fractional-shares",
        "Fractional Shares",
        "Fractional shares let you buy a slice of a stock or ETF with any "
        "dollar amount - $50 of a $500 stock buys 0.1 shares. This makes "
        "diversification possible with small balances and enables exact "
        "dollar-based investing and dividend reinvestment. Fractional "
        "holdings carry the same proportional economics as whole shares. "
        "Limitations: not all brokers offer them, transfers between brokers "
        "can force liquidation of fractions, and voting rights may not "
        "extend to fractional owners. For automated small-dollar investing, "
        "they're a genuine democratizing feature.",
    ),
    (
        "limit-vs-market-orders",
        "Market vs Limit Orders",
        "A market order executes immediately at the best available price - "
        "fast but you accept whatever the market gives, including slippage "
        "in volatile or thin trading. A limit order executes only at your "
        "price or better - price control but no execution guarantee. For "
        "liquid ETFs and large-caps during market hours, market orders are "
        "usually fine; for thinly traded stocks, large orders, or volatile "
        "moments, limit orders protect you. Never place market orders "
        "outside regular hours when spreads widen. Stop orders trigger at a "
        "price then become market orders - they don't guarantee the trigger "
        "price in a gap-down.",
    ),
    (
        "stop-loss-orders",
        "Stop-Loss Orders: Uses and Limits",
        "A stop-loss automatically sells when a price falls to your trigger, "
        "capping losses without constant monitoring. The danger: in flash "
        "crashes or overnight gaps, your stop triggers at terrible prices - "
        "a stop at $90 can fill at $70 in a gap-down - and whipsaws routinely "
        "stop investors out just before rebounds. For long-term index "
        "investors, stop-losses often do more harm than good by converting "
        "temporary volatility into permanent losses. They suit traders with "
        "defined risk plans, not buy-and-hold retirement portfolios.",
    ),
    (
        "short-selling-basics",
        "Short Selling Basics",
        "Short selling means borrowing shares, selling them, and hoping to "
        "buy back cheaper - profiting from declines. Risk is asymmetric: "
        "gains cap at 100% (stock to zero) while losses are theoretically "
        "unlimited, plus you pay borrow fees and can be forced to cover in "
        "short squeezes (see meme-stock episodes). It's a professional "
        "trading tool, not an investing strategy - most individuals should "
        "express negative views by simply not owning, or via defined-risk "
        "options. If you must, position-size tiny and use hard exit rules.",
    ),
    (
        "compounding-frequency",
        "Compounding Frequency",
        "Compounding frequency - how often interest is calculated - matters "
        "modestly: $10,000 at 6% grows to $10,616.78 compounded annually "
        "vs $10,618.31 monthly vs $10,618.37 daily. The differences are "
        "small because the rate dominates; frequency is a second-order "
        "effect. What matters far more: the rate itself, the time horizon, "
        "and additional contributions. Don't chase 'daily compounding' "
        "marketing - chase higher contributions, lower fees, and longer "
        "time in the market.",
    ),
    (
        "dollar-vs-percent",
        "Thinking in Dollars vs Percentages",
        "A 50% loss requires a 100% gain just to break even - percentages "
        "are asymmetric, and this math punishes volatility. A portfolio that "
        "swings +30%/-30% alternately goes nowhere fast (geometric drag). "
        "This is why 'average returns' mislead: an investment up 100% then "
        "down 50% has a 25% arithmetic average but 0% actual growth. Always "
        "evaluate with compound (geometric) returns over full cycles, and "
        "remember that avoiding large losses matters more than capturing "
        "every rally - defense compounds too.",
    ),
    (
        "interest-rates-fed",
        "Interest Rates and the Federal Reserve",
        "The Federal Reserve sets the federal funds rate, the benchmark that "
        "ripples through mortgages, credit cards, savings yields, and asset "
        "prices. When the Fed raises rates to fight inflation, borrowing "
        "costs rise, bond prices fall, and growth-stock valuations compress "
        "(future earnings are discounted more heavily). When it cuts, the "
        "reverse happens. Markets move more on expectations of Fed policy "
        "than on the decisions themselves - 'don't fight the Fed' reflects "
        "how powerfully liquidity shapes returns. Long-term investors should "
        "understand the mechanism but not trade on Fed headlines.",
    ),
    (
        "recession-basics",
        "Recessions and Your Portfolio",
        "A recession is a broad economic contraction - falling output, rising "
        "unemployment - typically lasting months, not years. Stocks usually "
        "fall before recessions are declared and recover before they end; "
        "waiting for 'all clear' headlines means missing the rebound. The "
        "average bear market since WWII lasted about a year with ~35% "
        "declines, followed by longer bull markets. Recession prep is "
        "structural, not tactical: an emergency fund, appropriate stock/bond "
        "mix, and continued contributions (which buy shares cheaply). "
        "Predicting recessions reliably is a fool's errand - even "
        "professional economists mostly miss them in real time.",
    ),
    (
        "bear-vs-bull-markets",
        "Bull vs Bear Markets",
        "A bull market is a sustained rise (commonly +20% from lows); a bear "
        "market is a sustained fall (-20% from highs). Bull markets last "
        "years on average; bears last months. Every bear market in U.S. "
        "history has eventually been erased by a subsequent bull - but "
        "'eventually' can mean years, which is why time horizon determines "
        "how much equity risk you can take. Bear markets feel permanent "
        "while you're in them; zooming out to century-scale charts is the "
        "antidote to panic. Corrections (-10%) are routine noise, occurring "
        "roughly annually.",
    ),
    (
        "market-timing",
        "Why Market Timing Fails",
        "Market timing requires two correct calls - when to sell and when to "
        "buy back - and missing just the 10 best days in a decade can cut "
        "total returns roughly in half, because the best days cluster near "
        "the worst. Dalbar's investor-behavior studies consistently show the "
        "average equity investor earns far less than the funds they own, "
        "largely from timing attempts. Professionals with full-time research "
        "teams fail at it persistently. The winning alternative is boring: "
        "set an allocation, automate contributions, rebalance periodically, "
        "and ignore forecasts.",
    ),
    (
        "behavioral-biases",
        "Behavioral Biases That Cost Investors Money",
        "Humans are wired to invest badly. Key biases: loss aversion (losses "
        "hurt ~2x more than equivalent gains, causing panic selling); "
        "recency bias (assuming recent trends continue); confirmation bias "
        "(seeking news that supports your holdings); overconfidence "
        "(trading too much); herding (buying manias, selling crashes); and "
        "anchoring (fixating on a past price). Defenses are structural: "
        "automation, written investment policy statements, diversified index "
        "funds, and pre-committed rebalancing rules that remove decisions "
        "from heated moments.",
    ),
    (
        "loss-aversion",
        "Loss Aversion and the Disposition Effect",
        "Loss aversion - feeling losses about twice as intensely as equal "
        "gains - drives the 'disposition effect': investors sell winners too "
        "early to lock in gains and hold losers too long to avoid admitting "
        "losses. This is backwards twice over: it cuts compounding short and "
        "concentrates the portfolio in its worst ideas, while also "
        "generating avoidable taxes on the winners sold. Countermeasures: "
        "judge positions by forward prospects not purchase price, use "
        "mechanical rebalancing, and in taxable accounts consider tax-loss "
        "harvesting losing positions instead of nursing them. Educational "
        "content only.",
    ),
    (
        "portfolio-beta",
        "Beta: Measuring Market Sensitivity",
        "Beta measures how much an investment moves with the overall market. "
        "Beta of 1.0 moves with the market; 1.5 is 50% more volatile; 0.5 "
        "is half as twitchy; negative beta (rare) moves oppositely. "
        "Utilities and consumer staples typically have low betas; tech and "
        "small-caps run high. A portfolio's weighted-average beta tells you "
        "its market sensitivity - a 0.8-beta portfolio should fall ~16% in "
        "a 20% market drop. Beta says nothing about expected return by "
        "itself; pair it with alpha (excess return) and drawdown history for "
        "a fuller picture.",
    ),
    (
        "sharpe-ratio",
        "Sharpe Ratio: Return per Unit of Risk",
        "The Sharpe ratio = (portfolio return minus risk-free rate) divided "
        "by volatility. It answers: how much excess return am I getting per "
        "unit of bumpiness? Above 1.0 is generally good, above 2.0 excellent, "
        "below 1.0 subpar. It lets you compare a calm 6% strategy against a "
        "wild 12% one on risk-adjusted terms. Limitations: it punishes upside "
        "volatility equally, assumes normal return distributions (markets "
        "have fat tails), and is period-dependent. Use it to compare "
        "similar strategies, not as a lone buy signal.",
    ),
    (
        "standard-deviation",
        "Standard Deviation as a Risk Measure",
        "Standard deviation quantifies how widely returns scatter around "
        "their average. An investment averaging 8% with 15% standard "
        "deviation will land between -7% and +23% in roughly two-thirds of "
        "years. Stocks: ~15-20%; bonds: ~4-6%; cash: ~0%. It is the workhorse "
        "risk metric behind the Sharpe ratio and portfolio theory, but it "
        "treats upside and downside equally and misses 'tail risk' - rare, "
        "extreme events. Still, knowing an asset's typical wobble prevents "
        "surprise: if you can't tolerate +/-20% years, you own too much equity.",
    ),
    (
        "correlation",
        "Correlation and Why It Matters",
        "Correlation (-1 to +1) measures how assets move together. +1 means "
        "lockstep; 0 means unrelated; -1 means opposite. Diversification "
        "works by combining less-than-perfectly-correlated assets: a stock/"
        "bond mix is smoother than either alone because their correlation is "
        "low. The catch: correlations spike toward 1 in panics - exactly "
        "when you want diversification most - as 2008 showed. True "
        "diversifiers (Treasuries in deflationary scares) are rare and "
        "unreliable; size equity risk so you survive the moments correlation "
        "fails you.",
    ),
    (
        "tax-loss-harvesting",
        "Tax-Loss Harvesting (Educational Overview)",
        "Tax-loss harvesting means selling investments at a loss to offset "
        "realized capital gains (and up to $3,000/year of ordinary income), "
        "then buying a similar - but not 'substantially identical' - "
        "asset to maintain exposure. It doesn't eliminate taxes; it defers "
        "them by lowering your cost basis, which has time-value. Beware the "
        "wash-sale rule: repurchasing the same security within 30 days "
        "before or after the sale disallows the loss. Harvesting is most "
        "valuable in high-income years and volatile markets. This is general "
        "education, not tax advice - tax rules are complex and personal; "
        "consult a qualified tax professional.",
    ),
    (
        "capital-gains-basics",
        "Capital Gains Tax Basics (Educational Overview)",
        "When you sell an investment for more than you paid, the profit is a "
        "capital gain. Short-term gains (assets held 1 year or less) are "
        "taxed as ordinary income; long-term gains (over 1 year) get "
        "preferential rates (0%, 15%, or 20% federally depending on income, "
        "plus possible state tax and the 3.8% net investment income tax for "
        "high earners). This rate gap is why holding periods matter - "
        "flipping stocks yearly can nearly double your tax drag versus "
        "holding. Losses can offset gains. Retirement accounts (401(k), IRA) "
        "shield you from annual capital-gains tax entirely. Educational "
        "content only - not tax advice.",
    ),
    (
        "wash-sale-rule",
        "The Wash-Sale Rule (Educational Overview)",
        "The wash-sale rule disallows claiming a tax loss if you buy a "
        "'substantially identical' security 30 days before or after the "
        "sale - a 61-day window. Violations are common with automatic "
        "dividend reinvestment or when a spouse buys the same stock in "
        "another account. The disallowed loss isn't lost forever; it's added "
        "to the replacement shares' cost basis, deferring the benefit. To "
        "harvest cleanly, buy a similar-but-not-identical fund (e.g., swap "
        "one S&P 500 ETF for another provider's) or wait out the window. "
        "Educational content only - not tax advice.",
    ),
    (
        "hsa-basics",
        "HSA: The Triple-Tax-Advantaged Account (Educational Overview)",
        "Health Savings Accounts, available with high-deductible health "
        "plans, offer a rare triple tax benefit: deductible contributions, "
        "tax-free growth, and tax-free withdrawals for qualified medical "
        "expenses. Unlike FSAs, HSAs have no use-it-or-lose-it rule and the "
        "account is yours if you change jobs. After 65, withdrawals for "
        "non-medical expenses are taxed like a traditional IRA (no penalty), "
        "making the HSA a stealth retirement account: pay medical bills from "
        "cash, let the HSA compound, and reimburse yourself decades later "
        "from saved receipts. 2026 limits: $4,400 individual / $8,750 "
        "family. Educational content only.",
    ),
    (
        "529-plans",
        "529 College Savings Plans (Educational Overview)",
        "529 plans are tax-advantaged accounts for education: contributions "
        "grow tax-deferred and withdrawals for qualified education expenses "
        "(tuition, books, room and board) are federally tax-free; many "
        "states offer deductions for contributions. You remain the account "
        "owner and can change beneficiaries to another family member. "
        "Non-qualified withdrawals face income tax plus a 10% penalty on "
        "earnings. Recent rules allow up to $35,000 lifetime rollover of "
        "unused 529 funds to the beneficiary's Roth IRA. Start early - "
        "education inflation has outpaced general inflation for decades. "
        "Educational content only.",
    ),
    (
        "sequence-of-returns-risk",
        "Sequence of Returns Risk",
        "Two retirees with identical average returns can have wildly "
        "different outcomes depending on WHEN the bad years hit. A 30% crash "
        "in year one of retirement, while withdrawing spending money, "
        "permanently impairs the portfolio; the same crash at age 40 is a "
        "buying opportunity. This is sequence-of-returns risk, and it is "
        "the central argument for de-risking near retirement, keeping 1-2 "
        "years of spending in cash-like reserves, and using flexible "
        "withdrawal rules that cut spending after down years.",
    ),
    (
        "tax-efficient-fund-placement",
        "Tax-Efficient Fund Placement (Educational Overview)",
        "Asset location means putting each investment in the account type "
        "where it's taxed least. General rules: hold tax-inefficient assets "
        "(bonds, REITs, high-turnover funds) in tax-deferred accounts "
        "(401(k), traditional IRA); hold tax-efficient assets (broad-market "
        "index ETFs with qualified dividends) in taxable brokerage "
        "accounts; reserve Roth accounts for the highest-growth assets "
        "since withdrawals are tax-free. Municipal bonds suit taxable "
        "accounts for high earners. Placement is second-order to saving "
        "enough, but it can add meaningful after-tax return over decades. "
        "Educational content only.",
    ),
    (
        "debt-payoff-strategies",
        "Debt Payoff: Avalanche vs Snowball",
        "Two proven strategies for killing debt: the avalanche (pay minimums "
        "everywhere, throw extra cash at the highest interest rate first) "
        "and the snowball (attack the smallest balance first for quick "
        "wins). The avalanche saves more money mathematically; the snowball "
        "wins behaviorally for people who need momentum. Both beat minimum-"
        "only payments, where a $5,000 balance at 24% APR takes 7+ years and "
        "costs ~$4,000 in interest. General priority: kill high-interest "
        "debt before investing beyond the 401(k) match - a guaranteed 24% "
        "'return' from payoff beats any market bet.",
    ),
    (
        "high-yield-savings",
        "High-Yield Savings Accounts",
        "High-yield savings accounts (HYSAs) from online banks pay far more "
        "than traditional brick-and-mortar savings - often 4-5% when the Fed "
        "funds rate is elevated - with FDIC insurance up to $250,000 per "
        "depositor per bank. They are ideal parking spots for emergency "
        "funds and short-term goals: liquid, safe, and earning something. "
        "Rates are variable and fall when the Fed cuts. Watch for teaser "
        "rates, withdrawal limits, and transfer delays (1-3 business days). "
        "Never confuse 'high-yield' with 'high return' - after inflation, "
        "cash barely grows; its job is safety, not wealth-building.",
    ),
    (
        "cd-ladder",
        "CD Ladders",
        "A CD ladder splits cash across certificates of deposit maturing at "
        "staggered intervals (e.g., 1, 2, 3, 4, 5 years). As each rung "
        "matures, you reinvest at the longest term, capturing higher "
        "long-term rates while gaining annual liquidity. It beats locking "
        "everything in one long CD (no flexibility) or all in short CDs "
        "(reinvestment risk if rates fall). Best for money needed on a "
        "known schedule 1-5 years out. Compare against Treasury yields - "
        "Treasuries are state-tax-exempt and sometimes pay more than CDs.",
    ),
    (
        "annuity-basics",
        "Annuities Basics (Educational Overview)",
        "Annuities are insurance contracts that convert lump sums into "
        "income streams. Immediate annuities start paying right away - "
        "useful for longevity insurance in retirement. Deferred and variable "
        "annuities grow tax-deferred but often carry high fees (2-3%+ "
        "annually), surrender charges, and complexity that benefits the "
        "seller more than you. Simple single-premium immediate annuities "
        "(SPIAs) are the most defensible type; indexed and variable "
        "annuities deserve extreme skepticism and a fee audit. Never buy "
        "an annuity you can't explain simply. Educational content only.",
    ),
    (
        "estate-planning-basics",
        "Estate Planning Basics (Educational Overview)",
        "Estate planning isn't just for the wealthy: everyone needs a will "
        "(naming guardians for minor children), beneficiary designations on "
        "retirement accounts and insurance (these override wills), a durable "
        "power of attorney, and a healthcare directive. Without them, state "
        "law decides - slowly and expensively. Review beneficiaries after "
        "marriage, divorce, births, and deaths. For larger estates, trusts "
        "can avoid probate and manage tax exposure; the federal estate-tax "
        "exemption is historically high but scheduled to change. This is "
        "general education, not legal or tax advice - consult an attorney.",
    ),
    (
        "sep-ira",
        "SEP IRA and Solo 401(k) for the Self-Employed",
        "Self-employed workers lack employer plans but have powerful "
        "options. A SEP IRA allows contributions up to 25% of compensation "
        "(capped annually), easy to set up. A Solo 401(k) permits both "
        "employee deferrals ($24,500 in 2026) plus employer profit-sharing, "
        "often allowing larger total contributions than a SEP at the same "
        "income, plus Roth options and loan provisions. Both grow "
        "tax-deferred. The self-employed also pay both halves of Social "
        "Security/Medicare tax, making retirement contributions doubly "
        "valuable as deductions. Deadlines and calculations are fiddly - "
        "verify with a tax professional. Educational content only.",
    ),
    (
        "credit-score-basics",
        "Credit Scores Basics",
        "A credit score (FICO/VantageScore, 300-850) summarizes your "
        "creditworthiness. Biggest factors: payment history (35%), amounts "
        "owed/utilization (30%), length of history (15%), new credit (10%), "
        "mix (10%). Higher scores unlock lower mortgage, auto, and card "
        "rates - a 1% mortgage-rate difference on $400k costs ~$85,000 over "
        "30 years. Build credit by paying on time, keeping utilization under "
        "30% (under 10% is better), and keeping old cards open. Check "
        "reports free annually at AnnualCreditReport.com and dispute errors. "
        "You don't need to carry a balance or pay interest to build credit - "
        "that's a myth.",
    ),
]


def build() -> int:
    KB_DIR.mkdir(parents=True, exist_ok=True)
    for slug, title, body in ARTICLES:
        (KB_DIR / f"{slug}.md").write_text(f"# {title}\n\n{body}\n", encoding="utf-8")
    return len(ARTICLES)


if __name__ == "__main__":
    n = build()
    print(f"Wrote {n} articles to {KB_DIR}")
