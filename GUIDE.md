# DSE Analysis — Complete User Guide

Your complete reference for using the DSE MCP server with Claude. Covers example queries, how to read results, trading strategy playbooks, indicator explanations, and advanced workflows.

---

## Quick Start — Copy-Paste These Queries

### Market Scan Queries
```
Scan DSE for momentum trades
Scan top stocks for swing trading
Scan for mean reversion opportunities — oversold stocks to buy
Scan for breakout setups, then run full analysis on the top 3
Scan for long-term investments and filter by P/E from company info
Scan top 30 stocks for all strategies and rank by best score
```

### Single Stock Analysis
```
Run full analysis on BRACBANK
Give me a complete technical analysis of GRAMEENPHONE
Is SQURPHARMA in a bullish trend? Check RSI and MACD
Show me Fibonacci support levels for BATBC
Give me an Ichimoku cloud analysis for ISLAMIBANK
What are the pivot point levels for RENATA today?
```

### Market Overview
```
How is the DSE market doing today?
What are the top 10 gainers on DSE right now?
What are the biggest losers today?
Show me the live price of DUTCHBANGLA
Get company fundamentals for SQURPHARMA — P/E, EPS, NAV
```

### Strategy-Specific Queries
```
Find CANSLIM setups — scan for breakouts then check company info on top results
Which DSE stocks are in Stage 2 uptrend by Weinstein's stage analysis?
Find stocks with RSI failure swings — oversold and turning up
Is there a Bollinger Band squeeze forming on any top DSE stocks?
Find stocks where MACD shows bullish divergence
Which stocks have Golden Cross (SMA50 crossing above SMA200)?
```

### Before-You-Trade Workflow
```
Step 1: "Get market summary" — check if DSEX is bullish or bearish
Step 2: "Scan top stocks for [your style]" — find candidates
Step 3: "Run full analysis on [SYMBOL]" — deep dive
Step 4: "Get Fibonacci levels for [SYMBOL]" — entry zone
Step 5: "Get pivot points for [SYMBOL]" — daily S/R levels
Step 6: "Analyze volatility for [SYMBOL]" — ATR stop-loss
Step 7: "Get company info for [SYMBOL]" — fundamental check
```

---

## How to Read Scan Results

When you run `scan_top_stocks`, each stock in the result has:

```
{
  "rank": 1,
  "symbol": "BRACBANK",
  "verdict": "BUY",           ← BUY / WATCH / AVOID
  "rating": "★★★★",           ← 1–5 stars
  "score": 12,                ← 0–15 (higher = stronger signal)
  "best_strategy": "momentum",← which strategy fits best
  "scores": {
    "momentum": 12,           ← how strong for each style
    "swing": 4,
    "long_term": 9,
    "breakout": 7,
    "mean_reversion": 2
  },
  "live_price": 46.50,
  "change_pct": 2.3,
  "trade_plan": {
    "entry": 46.50,           ← suggested entry price
    "stop_loss": 43.20,       ← cut loss here — NO exceptions
    "target_1": 51.45,        ← first take profit (2:1 R/R)
    "target_2": 56.40,        ← full target (3:1 R/R)
    "risk_pct": "7.1%",       ← how much you risk on this trade
    "risk_reward_t1": "1:1.5",
    "risk_reward_t2": "1:3",  ← for every 1 taka risk, make 3
    "note": "Enter on pullback to SMA20; ride the trend"
  },
  "indicators": {
    "rsi": 62.4,
    "trend": "UPTREND",
    "macd": "MACD above signal (bullish)",
    "bb": "MID",              ← SQUEEZE / UPPER / LOWER / MID
    "obv": "BULL"             ← BULL / BEAR / NEUTRAL
  }
}
```

### Score Ratings

| Score | Stars | Meaning |
|-------|-------|---------|
| 12–15 | ★★★★★ | Excellent — high conviction |
| 9–11 | ★★★★ | Good — solid setup |
| 6–8 | ★★★ | Moderate — some signals aligning |
| 3–5 | ★★ | Weak — wait for better setup |
| 0–2 | ★ | Poor — avoid |

### Trade Plan Logic by Strategy

| Strategy | Entry | Stop-Loss | Target 1 | Target 2 |
|----------|-------|-----------|----------|----------|
| Momentum | Current price | Below SMA20 or 2×ATR | 1.5× risk | 3× risk |
| Swing | Current (oversold) | 2×ATR below | BB middle (SMA20) | BB upper |
| Mean Reversion | Current (extreme oversold) | 1.5×ATR below | SMA20 | BB upper |
| Breakout | 0.5% above current | 1.5×ATR below | 2× risk | 4× risk |
| Long-Term | Current | SMA50 × 0.95 | +20% | +40% |

---

## Technical Indicators — What They Mean

### Trend: Moving Averages
```
Price
  │                     ┌── SMA200 (200-day, slow trend)
  │                   ┌─┘
  │               ┌───┘  ←── SMA50 (medium trend)
  │           ┌───┘
  │       ┌───┘  ←── SMA20 (fast trend, also BB middle)
  └───────┘
         Time →

  Golden Cross: SMA50 crosses ABOVE SMA200 → Strong long-term BUY
  Death Cross:  SMA50 crosses BELOW SMA200 → Strong long-term SELL
  Price > SMA20 > SMA50 > SMA200 → Perfect bullish alignment
```

### RSI (Relative Strength Index, 14-period)
```
100 ──────────────────────────────────────────
 70 ── OVERBOUGHT ── ← Potential reversal/sell
 60 ────────────────
 50 ── NEUTRAL ─────
 40 ────────────────
 30 ── OVERSOLD ──── ← Potential reversal/buy
  0 ──────────────────────────────────────────

  RSI Failure Swing (strongest RSI signal):
  RSI dips below 30 → bounces above 30 → dips but stays above 30
  → breaks the prior bounce high → BUY (confirmed reversal)

  RSI Divergence:
  Price makes new LOW but RSI makes HIGHER low → bullish divergence → BUY
  Price makes new HIGH but RSI makes LOWER high → bearish divergence → SELL
```

### MACD (12, 26, 9)
```
  MACD Line   = EMA(12) − EMA(26)      ← speed of trend
  Signal Line = EMA(9) of MACD Line    ← smoothed MACD
  Histogram   = MACD − Signal          ← momentum direction

  Signals (weakest → strongest):
  1. Histogram crosses zero            → momentum shift
  2. MACD crosses Signal Line          → trend shift
  3. MACD crosses Zero Line            → confirmed trend change
  4. Divergence from price             → STRONGEST signal

  Bullish divergence: price lower low, MACD higher low → BUY
  Bearish divergence: price higher high, MACD lower high → SELL
```

### Bollinger Bands (20-period, 2σ)
```
  Upper Band ────── SMA20 + 2 × StdDev    ← dynamic resistance
  Middle ────────── SMA20                 ← mean / first target
  Lower Band ────── SMA20 − 2 × StdDev   ← dynamic support

  BB SQUEEZE: Bands narrow to multi-month low
  → volatility compression → explosive move coming
  → direction confirmed by RSI + volume on breakout bar

  %B > 1.0 = price above upper band (breakout territory)
  %B < 0.0 = price below lower band (oversold territory)
  %B = 0.5 = price at middle band (mean reversion target)

  Walking the upper band = very strong uptrend (don't sell early)
```

### Ichimoku Cloud
```
  Tenkan-sen (9)  ─────── Fast signal (red/blue line)
  Kijun-sen (26)  ─────── Slow baseline
  Senkou A        ─ ─ ─ ─ Cloud edge (Tenkan+Kijun)/2 shifted 26 fwd
  Senkou B        ─ ─ ─ ─ Cloud edge (52-high+52-low)/2 shifted 26 fwd
  Chikou Span     ─────── Current close shifted 26 back

  3 confirmations for a strong buy signal:
  ① Price is ABOVE the cloud          → bullish bias
  ② Tenkan is ABOVE Kijun             → short-term bullish
  ③ Chikou is ABOVE price 26 bars ago → trend confirmed

  Cloud color tells the future:
  GREEN cloud (Span A > B) = bullish road ahead
  RED cloud   (Span A < B) = bearish road ahead
  THICK cloud = strong support/resistance
  THIN cloud  = weak support/resistance (easy breakout)
```

### Fibonacci Retracement
```
  Swing High ─── 0%
              ── 23.6%  ← minor retracement (very strong trend)
              ── 38.2%  ← first pullback support
              ── 50.0%  ← psychological level
              ── 61.8%  ← GOLDEN RATIO ★ strongest support/buy zone
              ── 78.6%  ← deep retracement (last defense)
  Swing Low  ─── 100%   ← full retracement (trend reversal)

  Extension targets (after continuation breakout):
              ── 127.2% ← first extension
              ── 161.8% ← main Fibonacci target ★
              ── 261.8% ← major extension

  Best setups: Fib 61.8% + RSI oversold + volume divergence = high-probability buy
  Confluence: Fib level aligns with pivot point = extra strong S/R
```

### OBV (On-Balance Volume)
```
  CONFIRMED UPTREND:   Price UP + OBV UP     = bulls in control
  BEARISH DIVERGENCE:  Price UP + OBV DOWN   = distribution, exit soon
  BULLISH DIVERGENCE:  Price DOWN + OBV UP   = accumulation, buy signal
  CONFIRMED DOWNTREND: Price DOWN + OBV DOWN = bears in control

  OBV is the "smart money tracker" — volume never lies
```

### ATR (Average True Range) — Position Sizing & Stop-Loss
```
  ATR = average of true price range over 14 periods
  
  Stop-loss formula:  Entry − (2 × ATR)
  Position size:      (Account × 1%) / (Entry − Stop)
  
  Example:
  Account = 100,000 BDT
  Entry   = 50.00
  ATR     = 2.00
  Stop    = 50.00 − (2 × 2.00) = 46.00
  Risk/share = 4.00
  Position = (100,000 × 1%) / 4.00 = 250 shares
```

---

## Trading Style Playbooks

### Momentum Trading (weeks to 2 months)

**What you're looking for:** Stocks with explosive price + volume acceleration — buy strength, not weakness.

**Ideal Setup Checklist:**
```
✓ RSI: 55–72 (strong but room to grow)
✓ MACD: Crossed above signal, above zero line
✓ Volume: 1.5x–3x above 20-day average
✓ Trend: Price above SMA20 and SMA50
✓ Price: Near 52-week high OR breaking to new high
✓ OBV: Rising — confirms institutional buying
✓ BB: Not at upper band yet (has room)
```

**Entry technique:** Wait for a 1–3 day pullback to SMA9 or SMA20 on declining volume, then enter when volume picks back up (pocket pivot).

**DSE query:**
```
Scan DSE for momentum trades
Then: Run full analysis on [top result] to confirm
Then: Get pivot points for [SYMBOL] for intraday entry
```

**Exit rules:**
- Partial profit at Target 1 (sell 50%)
- Move stop to break-even after Target 1 hit
- Hold remainder for Target 2 with trailing stop at SMA20

---

### Swing Trading (2–10 days)

**What you're looking for:** Stocks pulling back within an uptrend to support — buy the dip.

**Ideal Setup Checklist:**
```
✓ RSI: 30–45 (pulling back but not broken)
✓ MACD histogram: turning less negative (momentum slowing)
✓ Price: At Bollinger Band lower OR Fibonacci 38.2%–61.8% support
✓ Volume: DECLINING on the pullback (sellers exhausted)
✓ Trend: SMA50 > SMA200 (major trend still up)
✓ OBV: Rising while price falls = smart money holding
```

**Entry technique:** Wait for first green candle at support with volume expansion. Don't chase — if you miss it, move on.

**DSE query:**
```
Scan top stocks for swing trading
Then: Get Fibonacci levels for [top result]
Then: Analyze volume for [SYMBOL] — check if OBV diverging bullishly
```

**Exit rules:**
- Target 1 = BB middle (SMA20) — take 50% profit
- Target 2 = prior swing high or BB upper
- Stop = 2× ATR below entry

---

### Long-Term / Position Trading (3 months – 2 years)

**What you're looking for:** Stage 2 uptrends with improving fundamentals. Buy quality and hold.

**Ideal Setup Checklist:**
```
✓ Stage Analysis: In Stage 2 (price above rising SMA200)
✓ Golden Cross: SMA50 > SMA200 (confirmed)
✓ RSI: Consistently above 50
✓ Ichimoku: Price above green cloud
✓ OBV: Consistent long-term uptrend
✓ Fundamentals: P/E reasonable, EPS growing, NAV rising YoY
✓ Sector: In favor (banking recovery, pharma growth, etc.)
```

**Entry technique:** Buy any meaningful pullback to SMA50 while long-term trend is intact. Add to winners, never to losers.

**DSE query:**
```
Scan for long-term investments
Then: Get company info for top 5 results — filter by P/E < 15
Then: Get Ichimoku cloud for the best fundamentals stock
```

**Exit rules:**
- Exit when price closes below SMA200 for 2 consecutive weeks
- Review quarterly — is the fundamental story still intact?

---

### Breakout Trading (days to weeks)

**What you're looking for:** Explosive moves out of consolidation on high volume.

**Ideal Setup Checklist:**
```
✓ Consolidation: 3+ weeks of tight sideways action
✓ BB SQUEEZE: Bollinger Band width at multi-month low
✓ Volume: DRYING UP during consolidation (no supply)
✓ Breakout bar: Close above resistance on 2x+ average volume
✓ RSI: 50–68 at breakout moment
✓ MACD: Positive and rising
✓ Price: Near or at 52-week high (minimal overhead resistance)
```

**Entry technique:** Buy the breakout candle's close, or place a buy-stop order 0.5% above the resistance level.

**DSE query:**
```
Scan for breakout setups
Then: Analyze volatility for top results — look for BB squeeze
Then: Run full analysis on the squeeze candidates
```

**Exit rules:**
- If price falls back BELOW the breakout level → immediate exit (failed breakout)
- Target 1 = 2× risk (2:1 R/R)
- Target 2 = 4× risk (4:1 R/R) using Fibonacci extensions

---

### Mean Reversion (1–5 days)

**What you're looking for:** Extreme oversold conditions in healthy stocks — snap-back to the mean.

**Ideal Setup Checklist:**
```
✓ RSI: Below 30 (extreme oversold)
✓ BB: Price at or below lower band
✓ Selling Climax: Huge volume on the down day (panic selling)
✓ OBV: Bullish divergence (price lower, OBV higher = accumulation)
✓ Market context: DSEX not in a crash
✓ Fundamental: Company is NOT fundamentally broken
✓ Stochastic: Also oversold (<20) and turning up
```

**Entry technique:** Enter the first day RSI bounces back above 30, or the first green candle after the selling climax. Very tight stop.

**DSE query:**
```
Scan for mean reversion opportunities — oversold stocks to buy
Then: Analyze volume for top results — confirm OBV divergence
```

**Exit rules:**
- Target = SMA20 (BB middle) — this is the "mean" you're reverting to
- Full exit at BB upper if the bounce is strong
- Stop = 1.5× ATR below entry — tight, it's a short-term trade

---

## World-Famous Strategy Quick Reference

| Strategist | Strategy | Core Rule | Best For |
|------------|----------|-----------|---------|
| **William O'Neil** | CANSLIM | Best fundamentals + technical breakout + heavy volume | Growth stocks, breakouts |
| **Jesse Livermore** | Pivotal Points | Buy the breakout from consolidation; add to winners only | Momentum, trend following |
| **Warren Buffett** | Quality Value | Wonderful company at fair price, hold forever | Long-term investing |
| **Benjamin Graham** | Deep Value | Market price below Graham Number; P/E < 15 | Value, low P/E stocks |
| **Richard Donchian** | Turtle Trading | Buy 20-day/55-day highs; sell 10-day/20-day lows | Trend breakouts |
| **Stan Weinstein** | Stage Analysis | Only buy Stage 2 stocks (above rising SMA200) | All styles |
| **Mark Minervini** | SEPA + VCP | All 8 moving average criteria + volatility contraction | Growth momentum |
| **Nicolas Darvas** | Box Theory | Buy breakout above the box on heavy volume | Breakout trading |
| **Gerald Appel** | MACD | Crossovers, zero-line crosses, divergences | Trend + momentum |
| **Welles Wilder** | RSI | Oversold bounce, failure swings, divergences | Mean reversion, momentum |
| **John Bollinger** | BB Squeeze | Buy squeeze breakout; walk the upper band in trends | Volatility breakouts |
| **Ichimoku** | Cloud Trading | All 3 signals confirmed (price, TK cross, Chikou) | Trend confirmation |
| **Fibonacci** | Retracement | Buy at 61.8% golden ratio pullback | Swing, entry timing |
| **Elliott Wave** | Wave Count | Buy start of Wave 3; exit Wave 5 with divergence | Position trading |
| **Tom Williams** | VSA | Follow smart money through volume/price relationship | All styles |

---

## Advanced Power Queries

### Multi-Stock Comparison
```
Compare BRACBANK and DUTCHBANGLA — run full analysis on both and tell me which to buy
Which of the top 5 gainers today has the best momentum score?
Scan for momentum trades then rank the top 3 by risk/reward ratio
```

### Strategy-Specific Screening
```
Find DSE stocks with RSI below 30 AND price at BB lower band — mean reversion buys
Find stocks with Golden Cross AND price above Ichimoku cloud — long-term buys
Find breakout stocks where BB squeeze just ended on high volume
Find stocks where MACD shows bullish divergence but price hasn't moved up yet
Which stocks have OBV rising while price is falling — smart money accumulation?
```

### Risk Management Queries
```
I want to buy BRACBANK — what's my stop-loss and position size for 100,000 BDT account?
Analyze volatility for SQURPHARMA — give me ATR-based stop-loss at 2x ATR
If I risk 1% of 200,000 BDT on GRAMEENPHONE, how many shares should I buy?
```

### Full Pre-Trade Analysis (recommended workflow)
```
"Give me a complete pre-trade analysis on BATBC:
 1. Market summary first
 2. Full technical analysis
 3. Fibonacci levels for entry zones
 4. Pivot points for today's S/R
 5. Company info for fundamental check
 6. Suggested entry, stop-loss, and targets"
```

### Sector Analysis
```
Which banking stocks on DSE are in Stage 2 uptrend?
Compare pharma stocks — SQURPHARMA vs RENATA vs BEXIMCO — which is technically strongest?
Which sector is leading today based on top gainers?
```

---

## Risk Management Rules — Never Skip

```
1. 1% Rule       Never risk more than 1–2% of total capital per trade
                 Position Size = (Capital × 1%) / (Entry − Stop)

2. ATR Stop      Stop = Entry − (2 × ATR). Never use round numbers.
                 Example: Entry 50.00, ATR 2.00 → Stop = 46.00

3. Cut losses    Exit at 7–8% loss — no hoping, no averaging down

4. R/R minimum   Only take trades with 1:2 or better risk/reward
                 If R/R is worse than 1:2, skip the trade

5. Market filter If DSEX is in a downtrend, reduce size by 50%
                 Only trade the strongest stocks in a weak market

6. Add to winners Only add to positions that are already profitable
                 Never average down on a losing trade

7. Sector limit  Never put more than 25% in one sector

8. Trailing stop After +15% gain, move stop to break-even
                 After +25%, trail stop at SMA20 close

9. Earnings risk Don't hold into unknown earnings — large gap risk

10. 3 strikes    If 3 consecutive trades lose, take a 1-week break
                 Review what went wrong before re-entering
```

---

## DSE Market Reference

| Topic | Details |
|-------|---------|
| **Market Hours** | Sunday–Thursday, 10:00 AM – 2:30 PM (BST = UTC+6) |
| **Best scan time** | 11:00 AM – 12:00 PM (after opening volatility settles) |
| **Settlement** | T+2 (buy today, pay in 2 business days) |
| **Circuit breaker** | ±10% daily limit per stock (floor and ceiling) |
| **Index** | DSEX (broad), DS30 (top 30), DSES (Shariah) |
| **Most liquid stocks** | BRACBANK, GRAMEENPHONE, BATBC, SQURPHARMA, DUTCHBANGLA, RENATA, ISLAMIBANK, OLYMPIC, CITYBANK, BERGER |
| **High dividend** | BATBC, BERGER, MARICO, OLYMPIC (consumer goods) |
| **High growth** | RENATA, SQURPHARMA (pharma), BRACBANK (banking) |
| **Typical ATR range** | 1–5% of price per day for liquid stocks |

### Market Condition → Strategy Map

| DSEX Condition | Best Strategies | Avoid |
|----------------|----------------|-------|
| Strong uptrend | Momentum, Breakout, Long-term | Mean reversion (misses the trend) |
| Sideways/choppy | Mean Reversion, Swing | Momentum, Breakout |
| Downtrend | Mean Reversion (very selective), Cash | Long-term buys |
| Recovery from low | Swing + Long-term | Breakout (needs confirmation) |

---

## Indicator Cheat Sheet

| Indicator | Strong BUY signal | Strong SELL signal |
|-----------|------------------|--------------------|
| RSI | < 30 oversold OR failure swing up | > 70 overbought OR failure swing down |
| MACD | Bullish crossover + above zero + bullish divergence | Bearish crossover + below zero + bearish divergence |
| Bollinger Bands | Price bouncing off lower band; squeeze breakout up | Price rejected at upper band repeatedly |
| Ichimoku | Above cloud + TK bullish + Chikou bullish (3 confirmations) | Below cloud + TK bearish + Chikou bearish |
| OBV | Rising during price rise (confirmed uptrend) | Falling during price rise (bearish divergence) |
| Stochastic | < 20 and %K crosses above %D | > 80 and %K crosses below %D |
| SMA Cross | SMA50 crosses above SMA200 (Golden Cross) | SMA50 crosses below SMA200 (Death Cross) |
| Fibonacci | Price at 61.8% holding with RSI oversold | Price at 0% (Fib 0) failing — sell |
| Volume | 2x+ average on up candle = conviction | High volume on down candle = distribution |
| ATR | Low ATR after squeeze = move coming | Very high ATR = climax / exhaustion |
