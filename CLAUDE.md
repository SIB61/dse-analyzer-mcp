# DSE Analysis — Strategy Reference

This file is automatically loaded by Claude Code every time you open this project.
For other MCP clients (Cursor, Windsurf, Zed, etc.), paste its contents as a system prompt or context file — the strategies and tool references are fully client-agnostic.

It contains the world's most famous trading strategies, scoring frameworks, and how to apply each using the DSE MCP tools available in this session.

---

## User Preferences (Always Apply)

**The user follows Shariah-compliant investing.** Apply these rules in every response, unprompted:

1. **Default index is DSES** — whenever the user says "the market", "market index", or "market trend" without specifying an index, use **DSES** (Dhaka Stock Exchange Shariah Index), not DSEX or DS30.
2. **Default scan is Shariah-only** — `scan_top_stocks` has `shariah_only=True` by default. Do not override this unless the user explicitly asks to scan all DSE stocks.
3. **Prioritize Shariah stocks in all recommendations** — when the user asks for gainers, losers, or stock picks without specifying, mentally filter and lead with Shariah-compliant stocks from the results. Flag clearly if a stock is NOT Shariah-compliant.
4. **Exclude non-Shariah stocks from suggestions** — avoid recommending conventional interest-based banks (BRACBANK, DUTCHBANGLA, CITYBANK, PUBALI, NCCBANK, EBL, MTBL, UCBL, IFIC), tobacco companies (BATBC), or any stock known to fail Shariah screening.
5. **Use DSES as the market health benchmark** — when commenting on whether "the market is bullish/bearish", lead with the DSES index value from `get_market_summary`, not DSEX.
6. **When in doubt, ask** — if unsure whether a specific stock is Shariah-compliant, flag it and recommend the user verify with a Shariah advisor or DSE's official DSES component list.

**Known Shariah-compliant sectors on DSE:** Islamic banks, pharma, telecom, cement, steel, power/energy, textile, consumer goods (non-alcohol/tobacco).

---

---

## Available MCP Tools (Quick Reference)

| Tool | Use For |
|------|---------|
| `get_live_price(symbol)` | Real-time price |
| `get_historical_data(symbol, days)` | OHLCV history |
| `get_market_summary()` | DSEX/DS30 index overview |
| `get_top_gainers(n)` | Today's best performers |
| `get_top_losers(n)` | Today's worst performers |
| `get_company_info(symbol)` | P/E, EPS, NAV, market cap |
| `analyze_trend(symbol)` | SMA/EMA, Golden/Death Cross |
| `analyze_momentum(symbol)` | RSI, MACD, Stochastic |
| `analyze_volatility(symbol)` | Bollinger Bands, ATR |
| `analyze_volume(symbol)` | OBV, VWAP, volume trend |
| `get_fibonacci_levels(symbol)` | Fib retracements & extensions |
| `get_ichimoku_cloud(symbol)` | Full Ichimoku analysis |
| `get_pivot_points(symbol)` | S/R pivot levels |
| `full_analysis(symbol)` | All indicators + BUY/SELL verdict |
| `scan_top_stocks(style, top_n)` | Market scanner — ranked buy/sell list |

**`scan_top_stocks` styles:** `"momentum"` `"swing"` `"long_term"` `"breakout"` `"mean_reversion"` `"all"`

---

## World-Famous Trading Strategies

---

### 1. William O'Neil — CANSLIM (Growth Momentum)

**Philosophy:** Buy the best fundamental + technical breakouts. Only own the top 2% of stocks.

| Letter | Criteria | DSE Check |
|--------|----------|-----------|
| **C** — Current Earnings | EPS growth > 25% quarter-over-quarter | `get_company_info` → check EPS |
| **A** — Annual Earnings | 3-year EPS growth > 25%/yr | `get_company_info` → NAV trend |
| **N** — New Product/High | New 52-week high OR breakout to new high | `analyze_volatility` → BB upper break |
| **S** — Supply/Demand | Price rising on high volume | `analyze_volume` → volume 2x+ average |
| **L** — Leader | Top 10% in its sector by performance | `get_top_gainers` → sector leaders |
| **I** — Institutional | Increasing institutional accumulation | `analyze_volume` → OBV rising |
| **M** — Market Direction | Overall market in confirmed uptrend | `get_market_summary` → DSEX trending up |

**Entry Signal:**
- Stock breaks out of a sound base (cup-with-handle, flat base, double bottom) on volume 40%+ above average
- RSI 50–70 (strong but not overbought)
- Price at 52-week high or breaking to new high

**Exit Signal:** Cut loss at 7–8% below buy price. Take profit at 20–25% gain.

**DSE Query:** *"Find CANSLIM setups: scan top stocks for breakout style, then check company info on the top results for P/E and EPS"*

---

### 2. Jesse Livermore — Trend Following & Pivotal Points

**Philosophy:** "The market is never wrong. Opinions often are." Follow price — price leads fundamentals.

**Core Rules:**
1. Never trade against the major trend
2. Buy at pivotal points — the moment a stock breaks out of a consolidation
3. Add to winning positions only (never average down losers)
4. Never give back more than 10% of an open gain

**Pivotal Point Entry:**
```
Resistance level ──────────────────── ← Watch this level
         ↑
   Consolidation zone (3-6 weeks)
         ↓
Support level ──────────────────────

Entry: Price breaks ABOVE resistance on heavy volume
Stop:  Just below the resistance turned support
```

**DSE Tools:** `get_pivot_points` + `analyze_volume` → look for price at R1/R2 with volume spike

**Query:** *"Is [SYMBOL] breaking a pivotal resistance level? Check pivot points and volume"*

---

### 3. Warren Buffett — Value + Quality Investing (Long-Term)

**Philosophy:** "Buy wonderful companies at fair prices, not fair companies at wonderful prices."

**Buffett Checklist:**
- P/E ratio < sector average (or < 15 for value)
- Return on Equity (ROE) > 15% consistently
- Low debt (Debt/Equity < 0.5)
- Strong consistent earnings (NAV growing year over year)
- Durable competitive advantage ("moat") — market leader in sector
- Management that allocates capital well
- Price below intrinsic value (Margin of Safety ≥ 25%)

**Intrinsic Value Approximation:**
```
Fair Value = EPS × (8.5 + 2g) × 4.4 / Y
Where: g = expected growth rate (%), Y = current AAA bond yield
Margin of Safety: Buy at 25% below fair value
```

**DSE Application:**
- Use `get_company_info` for P/E, EPS, NAV
- Look for P/E < 10 in banking sector, < 15 in pharma/consumer
- NAV growing consistently over 3+ years
- High dividend yield stocks with stable earnings

**Query:** *"Find undervalued DSE stocks: scan for low P/E companies, then check if they're in an uptrend"*

---

### 4. Benjamin Graham — Deep Value (Margin of Safety)

**Philosophy:** "The stock market is a voting machine in the short run and a weighing machine in the long run."

**Graham Number (Maximum Fair Price):**
```
Graham Number = √(22.5 × EPS × Book Value per Share)
Buy when: Market Price < Graham Number (undervalued)
Ideal:     Market Price < 0.75 × Graham Number (deep value)
```

**Defensive Investor Criteria:**
1. P/E < 15
2. P/Book < 1.5 (ideally, P/E × P/B < 22.5)
3. Current ratio > 2 (financial health)
4. Earnings positive for 10 consecutive years
5. Dividend payment history (uninterrupted)
6. EPS growth ≥ 33% over 10 years

**DSE Application:** Best for banking and insurance stocks on DSE where book value data is available.

**Query:** *"Analyze ISLAMIBANK fundamentals — get company info and check if it's below Graham Number"*

---

### 5. Richard Donchian / Dennis & Eckhardt — Turtle Trading (Trend Breakout)

**Philosophy:** "The trend is your friend." Capture major moves by systematically trading breakouts.

**The Original Turtle Rules:**

**Entry:**
- System 1: Buy when price breaks above the 20-day high (short-term)
- System 2: Buy when price breaks above the 55-day high (long-term)
- Add units as price moves in your favor (pyramiding)

**Exit:**
- System 1: Exit when price breaks below the 10-day low
- System 2: Exit when price breaks below the 20-day low

**Position Sizing (N = ATR):**
```
Dollar Volatility = N × Price per Unit
Unit Size = 1% of account / Dollar Volatility
Maximum 4 units per market, 6 per correlated markets
```

**DSE Application:**
- Use `analyze_volatility` → ATR for position sizing
- Use `get_historical_data(days=60)` → check if at 20-day or 55-day high
- Volume confirmation: volume > 1.5× average on breakout

**Query:** *"Is BATBC at a 55-day high breakout? Check its ATR for position sizing"*

---

### 6. Stan Weinstein — Stage Analysis (Market Cycle)

**Philosophy:** Every stock moves through 4 stages. Never buy in Stage 3 or 4.

```
STAGE 1 — Basing/Accumulation
  ─────────────────────────────────────
  Price flat, volume low-declining
  Smart money accumulating quietly
  SMA150/200 flattening

STAGE 2 — Advancing (THE BUY ZONE) ★
  /‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾/
  Price breaking above Stage 1 resistance
  Volume expanding on up days
  Price > SMA150, SMA150 rising
  
STAGE 3 — Topping/Distribution
  ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
  Price volatile, choppy
  Volume high but price not advancing
  
STAGE 4 — Declining (NEVER BUY) ✗
  \________________________
  Price below falling SMA150/200
  Downtrends, lower highs & lows
```

**Entry:** Buy at the Stage 1→2 breakout with volume confirmation
**Exit:** Sell when price drops below rising 30-week SMA

**DSE Indicators:**
- Stage 2: Price > SMA200, SMA200 rising, RSI > 50, volume expanding
- Stage 4: Price < SMA200, SMA200 falling, RSI < 50

**Query:** *"What stage is GRAMEENPHONE in? Analyze trend — check if price is above SMA200 and SMA50"*

---

### 7. Mark Minervini — SEPA (Specific Entry Point Analysis)

**Philosophy:** Buy stocks with superior relative strength before they make major moves.

**SEPA Criteria (All 8 must be true):**
1. Price above SMA150 and SMA200
2. SMA150 above SMA200
3. SMA200 trending up for at least 1 month
4. SMA50 above SMA150 and SMA200
5. Price at least 25% above 52-week low
6. Price within 25% of 52-week high
7. Relative Strength vs market (outperforming DSEX)
8. Current price above SMA50

**VCP (Volatility Contraction Pattern):**
```
    │◄── contraction ──►│
    │  Price range       │
 ───┤  getting tighter  ├── BREAKOUT ►
    │  on declining vol  │
    │◄────────────────────┤
```
Look for 3 contractions, each smaller than the last.

**DSE Application:** Combines multiple `analyze_trend` + `analyze_volatility` checks

**Query:** *"Does SQURPHARMA meet Minervini's SEPA criteria? Check trend, all SMAs, and volatility contraction"*

---

### 8. Nicolas Darvas — Box Theory (Momentum Breakout)

**Philosophy:** Stocks move in "boxes." Buy the breakout of the top of the current box.

```
Previous box ───────────────
                             │
New box top ─────────────────┤←── BUY when price breaks here on volume
        ↑ ↑ ↑ ↑ ↑            │
New box  │││││││             │
bottom ──────────────────────┘

Rules:
- Define box: recent range between clear high and low
- Wait for close ABOVE the box top
- Set stop just below the box bottom
- If stopped out, wait for new box to form
```

**DSE Application:**
- Use `analyze_volatility` → Bollinger Band width (narrow = box forming)
- Use `get_pivot_points` → box top = R1, box bottom = Pivot/S1
- Volume must expand on the breakout bar

**Query:** *"Is [SYMBOL] forming a Darvas box? Check if Bollinger Bands are squeezing and price is near resistance"*

---

### 9. Gerald Appel — MACD Strategy (Trend + Momentum)

**Philosophy:** The MACD captures the difference between two trend-following moving averages, giving both trend and momentum in one indicator.

**MACD Trading Rules:**

**Signal Line Crossover:**
```
MACD Line ──────────────────────────────
               ↗ BUY: MACD crosses above Signal
Signal Line ──────────────────────────────
               ↘ SELL: MACD crosses below Signal
```

**Zero Line Crossover (stronger signal):**
- MACD crosses above 0 → Confirmed uptrend → BUY
- MACD crosses below 0 → Confirmed downtrend → SELL

**MACD Divergence (most powerful signal):**
```
Price making LOWER lows    → but MACD making HIGHER lows → BULLISH divergence (buy)
Price making HIGHER highs  → but MACD making LOWER highs → BEARISH divergence (sell)
```

**Multi-timeframe confirmation:**
- Weekly MACD bullish + Daily MACD bullish → high-confidence buy

**DSE Query:** *"Show MACD analysis for BRACBANK — is there a crossover or divergence?"*

---

### 10. J. Welles Wilder — RSI Strategy

**Philosophy:** Momentum always leads price. RSI failures and divergences are the most reliable signals.

**RSI Rules (14-period):**

| RSI Level | Signal | Action |
|-----------|--------|--------|
| > 70 | Overbought | Look to sell / take profit |
| 50–70 | Bullish momentum | Hold longs / look for entries on dips |
| 30–50 | Bearish momentum | Avoid longs / consider shorts |
| < 30 | Oversold | Look to buy / accumulate |

**RSI Failure Swing (Most Reliable):**
```
BULLISH FAILURE SWING:
RSI drops below 30 (oversold)   → then rises above 30
RSI dips again but STAYS above  → then breaks the prior high
                                    ↑ BUY signal here

BEARISH FAILURE SWING:
RSI rises above 70 (overbought) → then drops below 70
RSI rises again but STAYS below → then breaks the prior low
                                    ↓ SELL signal here
```

**RSI Divergence:**
- Price new high + RSI lower high = bearish divergence → SELL
- Price new low + RSI higher low = bullish divergence → BUY

**Query:** *"Is RSI showing a failure swing or divergence on ISLAMIBANK?"*

---

### 11. John Bollinger — Bollinger Band Strategies

**Philosophy:** Volatility is cyclical. After a squeeze comes an expansion. Bands are not overbought/oversold signals by themselves.

**Strategy 1 — The Squeeze (Best Setup)**
```
─────────────────────────────  ← Upper Band
 ║ bands ║                   ←── Normal width
─────────────────────────────  ← Middle (SMA20)
 ║ narrow║                   ←── SQUEEZE: bands touch
─────────────────────────────  ← Lower Band

Squeeze = BB Width at multi-month LOW
After squeeze → explosive directional move
Direction: determined by RSI, MACD, volume at breakout
```

**Strategy 2 — Walking the Band**
- Price touching upper band repeatedly = strong uptrend (don't sell just because it's at the upper band)
- "Walking the upper band" = very bullish sign

**Strategy 3 — W-Bottom (Double Bottom Buy)**
```
Price touches lower band (1st bottom)    → bounces to middle
Price dips again but HIGHER than 1st   → second low above lower band
RSI confirms (higher low too)            → BUY
```

**%B Indicator:**
- %B > 1.0 = price above upper band (breakout)
- %B < 0.0 = price below lower band (oversold)
- %B at 0.5 = price at middle band

**Query:** *"Is there a Bollinger Band squeeze on any top DSE stocks? Scan for breakout opportunities"*

---

### 12. Ichimoku Kinko Hyo — Complete Cloud Trading

**Philosophy:** One chart, complete picture — trend, momentum, support, resistance, and signals in one system.

**The 5 Components:**
```
Tenkan-sen (9)   ──────── Fast signal line (red)
Kijun-sen (26)   ──────── Slow baseline (blue)
Senkou Span A    ─ ─ ─ ─  Cloud top (shifted 26 ahead)
Senkou Span B    ─ ─ ─ ─  Cloud bottom (shifted 26 ahead)
Chikou Span      ──────── Lagging line (current close shifted 26 back)
```

**The 3 Signals (in order of strength):**

```
1. TK CROSS (weakest):
   Tenkan crosses above Kijun → weak buy
   Tenkan crosses below Kijun → weak sell

2. KUMO (CLOUD) BREAKOUT (medium):
   Price breaks above cloud  → medium buy
   Price breaks below cloud  → medium sell

3. EDGE-TO-EDGE (strongest — "3 confirmations"):
   Price above cloud         → bullish
   Tenkan above Kijun        → bullish
   Chikou above price 26 bars ago → bullish
   ALL THREE = strong buy signal ★
```

**Cloud Analysis:**
- Green cloud (Span A > B) ahead = bullish future
- Red cloud (Span A < B) ahead = bearish future
- Thick cloud = strong support/resistance
- Thin cloud = weak support/resistance (easy to break)

**Query:** *"Give me a full Ichimoku analysis on DUTCHBANGLA — do all three signals confirm a buy?"*

---

### 13. Fibonacci Trading Strategy

**Philosophy:** Markets retrace in Fibonacci proportions before continuing their primary trend.

**Key Levels:**
```
Swing High ──── 0%      ← Top of the move
             ── 23.6%   ← Minor retracement (strong uptrend)
             ── 38.2%   ← First support (moderate uptrend)
             ── 50.0%   ← Psychological midpoint
             ── 61.8%   ← GOLDEN RATIO — strongest support ★
             ── 78.6%   ← Deep retracement (last chance)
Swing Low  ──── 100%    ← Full retracement (trend reversal)

Extensions (projection targets after continuation):
             ── 127.2%  ← First extension target
             ── 161.8%  ← Main Fibonacci target ★
             ── 261.8%  ← Major extension target
```

**Entry Strategy:**
1. Identify a clear swing high and swing low
2. Wait for price to retrace to 38.2%, 50%, or 61.8%
3. Look for RSI oversold + MACD bullish divergence AT the Fib level
4. Enter with stop just below the Fib level
5. Target the next Fib extension (127.2% or 161.8%)

**Confluence (most powerful setups):**
- Fib level + Pivot Point at same price = strong S/R
- Fib 61.8% + Bollinger Band lower = very strong buy zone
- Fib 61.8% + RSI oversold + volume divergence = high-probability buy

**Query:** *"Where are the Fibonacci support levels for SQURPHARMA? Is the price near the 61.8% golden ratio?"*

---

### 14. Volume Spread Analysis (VSA) — Tom Williams

**Philosophy:** Price and volume tell the story of supply and demand. Smart money leaves footprints in the volume.

**Key VSA Signals:**

| Bar Type | Price | Volume | Meaning |
|----------|-------|--------|---------|
| Stopping Volume | Down bar, closes near high | Ultra-high | Smart money buying — reversal near |
| No Supply | Narrow range up bar | Low | No sellers — bullish continuation |
| No Demand | Narrow range up bar | Low | Buyers weak — bearish |
| Effort vs Result | Wide bar, big volume | High | Low close = distribution; High close = accumulation |
| Shakeout | Sharp down spike | High | Weak hands flushed — strong reversal signal |

**Accumulation vs Distribution:**
```
ACCUMULATION (Smart money buying quietly):
- Price moves sideways or slightly down
- Volume above average on DOWN days that close near HIGH
- OBV rising while price flat

DISTRIBUTION (Smart money selling):
- Price moves sideways or slightly up
- Volume above average on UP days that close near LOW
- OBV falling while price flat or rising
```

**Query:** *"Analyze volume for BRACBANK — is there accumulation or distribution happening?"*

---

### 15. Elliott Wave Theory

**Philosophy:** Markets move in repetitive wave patterns driven by crowd psychology.

**Basic Wave Count:**
```
     3
    /\
   /  \
  /  2 \    5
 /1    \/  /\
/        \/  \
─────────────  ← A
              \  /
               \/
               B (correction)

Impulse waves: 1, 3, 5 (with direction)
Corrective waves: 2, 4 (against direction)
ABC correction after 5-wave impulse
```

**Wave Characteristics:**
- Wave 3 is NEVER the shortest (usually the strongest)
- Wave 2 never retraces more than 100% of Wave 1
- Wave 4 never enters Wave 1's territory
- Wave 3 target: often 161.8% of Wave 1

**Practical Application (simplified):**
- Use Fibonacci levels to project wave targets
- Wave 3 starts = strong momentum buy after Wave 2 pulls back to 38.2–61.8% of Wave 1
- If RSI hits 80+ in wave 3 = normal; bearish divergence in wave 5 = prepare to exit

**Query:** *"Check historical data for RENATA over 2 years and identify if it's in a wave 3 or wave 5"*

---

## Trading Style Frameworks

---

### Momentum Trading (Weeks to 2 months)

**Goal:** Catch stocks with explosive price acceleration. Ride the wave while it lasts.

**Setup Criteria:**
```
✓ RSI: 55–75 (strong but not extreme)
✓ MACD: Above signal line AND above zero
✓ Volume: 1.5x–3x above 20-day average
✓ Trend: Price above SMA20 and SMA50
✓ Price: Breaking to new highs OR near 52-week high
✓ Sector: Sector in favor (check top gainers sector)
```

**Entry:** Intraday pullback to SMA9 or SMA20 on declining volume
**Exit:** RSI hits 75+ AND MACD shows divergence
**Stop-loss:** Below SMA20 (close basis)
**Risk/Reward:** Minimum 1:2

**DSE Query:** *"Scan DSE for momentum trades — scan_top_stocks with style momentum"*

---

### Swing Trading (2–10 days)

**Goal:** Capture one price swing from oversold/support to the next resistance.

**Setup Criteria:**
```
✓ RSI: 25–45 (pulling back in an uptrend)
✓ MACD: Histogram turning less negative (momentum shift)
✓ Price: At/near Bollinger Band lower OR Fibonacci 38.2–61.8% support
✓ Volume: Declining on the pullback (sellers exhausting)
✓ Trend: Overall trend is UP (SMA50 > SMA200)
✓ OBV: Rising while price pulls back (smart money holding)
```

**Entry:** First green bar after hitting support, confirmed by volume picking up
**Exit:** Bollinger Band middle (SMA20) OR prior swing high
**Stop-loss:** 2× ATR below entry
**Risk/Reward:** Minimum 1:3

**DSE Query:** *"Scan for swing trade setups — scan_top_stocks with style swing"*

---

### Long-Term / Position Trading (3 months – 2 years)

**Goal:** Capture the full extent of a major trend. Hold through minor pullbacks.

**Setup Criteria:**
```
✓ Stage Analysis: Stock in Stage 2 (uptrend)
✓ SMA200: Rising AND price above it
✓ SMA50: Above SMA200 (Golden Cross confirmed)
✓ RSI: Above 50 consistently
✓ Fundamentals: P/E reasonable, EPS growing, NAV rising
✓ Ichimoku: Price above cloud, cloud is green
✓ Volume: OBV in consistent uptrend
✓ Sector: Sector is in favor long-term (banking, pharma, telecom)
```

**Entry:** Any pullback to SMA50 or SMA200 while long-term trend intact
**Exit:** Close below SMA200 for 2 consecutive weeks
**Stop-loss:** 15% below entry (mental stop for long-term)
**Risk/Reward:** Target 3× to 10× potential

**DSE Query:** *"Scan for long-term investments — scan_top_stocks with style long_term, then get company info on top results"*

---

### Breakout Trading (Days to weeks)

**Goal:** Catch explosive moves as price breaks through key resistance with force.

**Setup Criteria:**
```
✓ Consolidation: 3+ weeks of tight price action (Bollinger Band squeeze)
✓ Volume: DRYING UP during consolidation (no supply)
✓ Breakout bar: Close above resistance on 2x+ average volume
✓ RSI: 50–70 at breakout (momentum but not overbought)
✓ MACD: Above signal line at breakout
✓ Price: Ideally near 52-week high (no overhead resistance)
```

**Entry:** On breakout bar close, OR 1–2% above resistance
**Exit:** 15–20% profit target OR if price falls back into consolidation
**Stop-loss:** Below breakout level (usually 3–5%)
**Risk/Reward:** Minimum 1:3

**DSE Query:** *"Scan for breakout opportunities — scan_top_stocks with style breakout"*

---

### Mean Reversion (1–5 days)

**Goal:** Buy extreme oversold conditions expecting a snap-back to the mean.

**Setup Criteria:**
```
✓ RSI: Below 30 (extreme oversold)
✓ Bollinger Band: Price at or below lower band
✓ Volume: Selling climax (very high volume on down day)
✓ OBV: Bullish divergence (price lower, OBV higher)
✓ Market: Overall market not in a crash/circuit-breaker
✓ Support: Price at known Fibonacci level or prior support
```

**Entry:** First day RSI turns back up from below 30
**Exit:** Price returns to SMA20 (Bollinger Band middle)
**Stop-loss:** 2× ATR below entry (tight)
**Risk/Reward:** 1:2 minimum (quick trade)

**Warning:** Never use mean reversion on fundamentally broken companies or stocks in Stage 4 decline.

**DSE Query:** *"Scan for mean reversion opportunities — scan_top_stocks with style mean_reversion"*

---

## Scoring System (Used by `scan_top_stocks`)

Each stock is scored 0–15 per trading style. Here's what the scores mean:

| Score | Rating | Action |
|-------|--------|--------|
| 12–15 | ★★★★★ Excellent | Strong signal — high conviction |
| 9–11 | ★★★★ Good | Solid setup — consider entry |
| 6–8 | ★★★ Moderate | Some signals aligning — watch |
| 3–5 | ★★ Weak | Only 1-2 signals — avoid |
| 0–2 | ★ Poor | No meaningful signal |

**For `full_analysis` confidence score:**
- > 70% confidence = Strong BUY or SELL
- 55–70% = Moderate signal
- < 55% = Neutral / Hold

---

## Master Workflow — Finding the Best Trades

### Step 1: Market Context
```
"Get market summary" → Is DSEX rising, falling, or sideways?
If DSEX is falling strongly → only trade mean reversion or defensive stocks
If DSEX is rising → momentum, breakout, and long-term setups work best
```

### Step 2: Scan for Candidates
```
"Scan top stocks for [momentum/swing/breakout/mean_reversion/long_term]"
→ Gets you a scored, ranked list of the most active DSE stocks
```

### Step 3: Deep Dive on Top Candidates
```
"Run full analysis on [TOP STOCK 1]"
"Run full analysis on [TOP STOCK 2]"
→ Detailed verdict with confidence score
```

### Step 4: Entry Confirmation
```
"Get Fibonacci levels for [SYMBOL]"     → Where to enter
"Get pivot points for [SYMBOL]"         → Intraday S/R
"Analyze volatility for [SYMBOL]"       → ATR for stop-loss
```

### Step 5: Fundamental Check (for long-term only)
```
"Get company info for [SYMBOL]"
→ P/E, EPS, NAV — confirm fundamentals match technical setup
```

### Step 6: Final Decision Framework
```
Technical score > 9  AND
Fundamental P/E reasonable  AND
Market trend aligned  AND
Risk/Reward > 1:2
→ ENTER the trade

Define before entering:
• Entry price
• Stop-loss (ATR-based or Fib level)
• Target (Fib extension or pivot R2/R3)
• Position size (1-2% of portfolio per trade)
```

---

## Risk Management Rules (Never Skip These)

1. **1% Rule:** Never risk more than 1–2% of total capital on one trade
2. **ATR Stop:** Stop-loss = Entry price − (2 × ATR). Never use round numbers.
3. **Position sizing:** Position Size = (Account × 1%) / (Entry − Stop)
4. **Cut losses at 7–8%** (O'Neil rule) — no exceptions, no hoping
5. **Never average down** in a losing position (averaging up in winners = OK)
6. **3:1 Risk/Reward** minimum — if you can't find a 3:1 setup, skip the trade
7. **Market filter:** If DSEX is in a downtrend, reduce position sizes by 50%
8. **Diversify sectors:** Never put > 25% in one sector
9. **Earnings rule:** Don't hold through unknown earnings events (volatility risk)
10. **Trailing stop:** Once up 15%+, move stop to break-even

---

## Quick Reference — Indicator Cheat Sheet

| Indicator | Bullish | Bearish | Neutral |
|-----------|---------|---------|---------|
| RSI | < 30 (oversold) or 50–70 (momentum) | > 70 (overbought) or 30–50 (weak) | 45–55 |
| MACD | Above signal, above zero, bullish cross | Below signal, below zero, bearish cross | Near zero |
| Bollinger | Price bouncing off lower band | Price rejected at upper band | Mid-band |
| Ichimoku | Above green cloud, TK bullish, Chikou above | Below red cloud | Inside cloud |
| OBV | Rising with price or bullish divergence | Falling with price or bearish divergence | Flat |
| Stochastic | < 20 and turning up | > 80 and turning down | 40–60 |
| SMA Cross | SMA50 > SMA200 (Golden Cross) | SMA50 < SMA200 (Death Cross) | SMAs crossing |
| Fibonacci | Price at 61.8% holding | Price breaking below 61.8% | Between levels |

---

## DSE-Specific Notes

- **Market Hours:** Sunday–Thursday, 10:00 AM – 2:30 PM (Bangladesh time / BST = UTC+6)
- **Settlement:** T+2 (trade today, settle in 2 business days)
- **Circuit Breaker:** Individual stock ±10% daily limit (floor/ceiling)
- **Top Sectors by Market Cap:** Banking, Pharma/Chemicals, Telecom, Fuel/Power, Textile
- **Most Liquid Stocks:** BRACBANK, GRAMEENPHONE, BATBC, SQURPHARMA, DUTCHBANGLA, RENATA, ISLAMIBANK, OLYMPIC, CITYBANK, BERGER
- **Dividend Stocks (high yield):** BATBC, BERGER, MARICO, OLYMPIC (consumer goods sector)
- **Growth Stocks (high EPS growth):** RENATA, SQURPHARMA (pharma), BRACBANK (banking)
- **bdshare data is scraped live** — works best during and just after market hours
