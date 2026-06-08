"""DSE Analysis MCP Server — exposes DSE data and technical analysis tools via MCP."""
import json
from datetime import datetime, timedelta

from mcp.server.fastmcp import FastMCP

import dse_data as dse
import technical_analysis as ta_lib

mcp = FastMCP("DSE Analysis")

_PROJECT_DIR = __import__("os").path.dirname(__import__("os").path.abspath(__file__))


def _json(obj) -> str:
    return json.dumps(obj, indent=2, default=str)


def _load_history(symbol: str, days: int = 365) -> tuple:
    """Returns (df, error_str). Historical archive + today's live candle merged."""
    start, end = dse.default_date_range(days)
    df = dse.get_historical_data_with_live(symbol, start, end)
    if df.empty:
        return None, f"No historical data found for {symbol} in the last {days} days."
    return df, None


# ---------------------------------------------------------------------------
# DSE Data Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def get_live_price(symbol: str) -> str:
    """
    Get real-time live price for a DSE-listed stock.

    Args:
        symbol: DSE trading code, e.g. BRACBANK, GRAMEENPHONE, SQURPHARMA
    """
    result = dse.get_live_price(symbol)
    return _json(result)


@mcp.tool()
def get_historical_data(symbol: str, start_date: str = "", end_date: str = "", days: int = 365) -> str:
    """
    Get historical OHLCV (Open, High, Low, Close, Volume) candles for a DSE stock.

    Args:
        symbol: DSE trading code
        start_date: Start date YYYY-MM-DD (optional, defaults to `days` ago)
        end_date: End date YYYY-MM-DD (optional, defaults to today)
        days: Number of days of history if start_date not provided (default 365)
    """
    if not start_date or not end_date:
        start_date, end_date = dse.default_date_range(days)
    df = dse.get_historical_data(symbol, start_date, end_date)
    if df.empty:
        return _json({"error": f"No data for {symbol} between {start_date} and {end_date}"})
    records = df.reset_index().tail(100).to_dict(orient="records")
    return _json({
        "symbol": symbol.upper(),
        "from": start_date,
        "to": end_date,
        "candles": len(df),
        "data": records,
    })


@mcp.tool()
def get_market_summary() -> str:
    """Get DSE market summary — DSEX, DS30, and DSES index values with daily change."""
    result = dse.get_market_summary()
    return _json(result)


@mcp.tool()
def get_top_gainers(n: int = 10) -> str:
    """
    Get today's top gaining stocks on DSE.

    Args:
        n: Number of stocks to return (default 10)
    """
    result = dse.get_top_gainers(n)
    return _json(result)


@mcp.tool()
def get_top_losers(n: int = 10) -> str:
    """
    Get today's top losing stocks on DSE.

    Args:
        n: Number of stocks to return (default 10)
    """
    result = dse.get_top_losers(n)
    return _json(result)


@mcp.tool()
def get_all_live_prices() -> str:
    """Get current prices for all DSE-listed stocks in one call."""
    result = dse.get_all_live_prices()
    return _json(result)


@mcp.tool()
def get_company_info(symbol: str) -> str:
    """
    Get fundamental data for a DSE company — P/E ratio, EPS, NAV, market cap.

    Args:
        symbol: DSE trading code
    """
    result = dse.get_company_info(symbol)
    return _json(result)


# ---------------------------------------------------------------------------
# Technical Analysis Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def analyze_trend(symbol: str, days: int = 365) -> str:
    """
    Trend analysis using Moving Averages (SMA 20/50/200, EMA 9/21/55),
    Golden Cross / Death Cross detection, and overall trend direction.

    Args:
        symbol: DSE trading code
        days: Number of historical days to analyze (default 365)
    """
    df, err = _load_history(symbol, days)
    if err:
        return _json({"error": err})
    result = ta_lib.analyze_trend(df)
    result["symbol"] = symbol.upper()
    return _json(result)


@mcp.tool()
def analyze_momentum(symbol: str, days: int = 365) -> str:
    """
    Momentum analysis: RSI (14), MACD (12,26,9), Stochastic Oscillator (14,3,3),
    Williams %R, Rate of Change — with buy/sell signals and divergence detection.

    Args:
        symbol: DSE trading code
        days: Number of historical days to analyze (default 365)
    """
    df, err = _load_history(symbol, days)
    if err:
        return _json({"error": err})
    result = ta_lib.analyze_momentum(df)
    result["symbol"] = symbol.upper()
    return _json(result)


@mcp.tool()
def analyze_volatility(symbol: str, days: int = 365) -> str:
    """
    Volatility analysis: Bollinger Bands (20,2) with squeeze detection,
    ATR (14) for stop-loss calculation, historical volatility.

    Args:
        symbol: DSE trading code
        days: Number of historical days to analyze (default 365)
    """
    df, err = _load_history(symbol, days)
    if err:
        return _json({"error": err})
    result = ta_lib.analyze_volatility(df)
    result["symbol"] = symbol.upper()
    return _json(result)


@mcp.tool()
def analyze_volume(symbol: str, days: int = 365) -> str:
    """
    Volume analysis: OBV (On-Balance Volume) with divergence, VWAP (20-period),
    Volume moving average, volume vs average ratio.

    Args:
        symbol: DSE trading code
        days: Number of historical days to analyze (default 365)
    """
    df, err = _load_history(symbol, days)
    if err:
        return _json({"error": err})
    result = ta_lib.analyze_volume(df)
    result["symbol"] = symbol.upper()
    return _json(result)


@mcp.tool()
def get_fibonacci_levels(symbol: str, days: int = 180, lookback: int = 60) -> str:
    """
    Fibonacci retracement and extension levels based on recent swing high/low.
    Identifies nearest support and resistance levels.

    Args:
        symbol: DSE trading code
        days: Historical data period in days (default 180)
        lookback: Candles to look back for swing high/low (default 60)
    """
    df, err = _load_history(symbol, days)
    if err:
        return _json({"error": err})
    result = ta_lib.fibonacci_levels(df, lookback=lookback)
    result["symbol"] = symbol.upper()
    return _json(result)


@mcp.tool()
def get_ichimoku_cloud(symbol: str, days: int = 365) -> str:
    """
    Full Ichimoku Kinko Hyo analysis: Tenkan-sen, Kijun-sen, Senkou Span A & B,
    Chikou Span. Cloud color, TK cross signals, price vs cloud position.

    Args:
        symbol: DSE trading code
        days: Historical days (minimum 52 candles needed, default 365)
    """
    df, err = _load_history(symbol, days)
    if err:
        return _json({"error": err})
    result = ta_lib.ichimoku_cloud(df)
    result["symbol"] = symbol.upper()
    return _json(result)


@mcp.tool()
def get_pivot_points(symbol: str, days: int = 90) -> str:
    """
    Classic pivot points for support and resistance: Pivot, R1/R2/R3, S1/S2/S3.

    Args:
        symbol: DSE trading code
        days: Historical data period (default 90)
    """
    df, err = _load_history(symbol, days)
    if err:
        return _json({"error": err})
    result = ta_lib.pivot_points(df)
    result["symbol"] = symbol.upper()
    return _json(result)


@mcp.tool()
def full_analysis(symbol: str, days: int = 365) -> str:
    """
    Comprehensive technical analysis combining ALL indicators:
    - Trend: SMA/EMA, Golden/Death Cross
    - Momentum: RSI, MACD, Stochastic, Williams %R
    - Volatility: Bollinger Bands, ATR
    - Volume: OBV, VWAP
    - Fibonacci retracement levels
    - Ichimoku Cloud
    - Pivot Points
    - Aggregated BUY/SELL/HOLD verdict with confidence score.

    Args:
        symbol: DSE trading code, e.g. BRACBANK, GRAMEENPHONE, BATBC
        days: Historical days for analysis (default 365)
    """
    df, err = _load_history(symbol, days)
    if err:
        return _json({"error": err})
    result = ta_lib.full_analysis(df, symbol=symbol.upper())
    return _json(result)


@mcp.tool()
def scan_top_stocks(trading_style: str = "all", top_n: int = 20, shariah_only: bool = True) -> str:
    """
    Scan and score DSE stocks using world-famous strategies.
    Returns a ranked list of BUY/WATCH/AVOID candidates with strategy scores.

    This tool:
      1. Fetches live prices and picks the most active stocks by volume
      2. If shariah_only=True (default), filters to DSES Shariah-compliant stocks only
      3. Downloads 90 days of OHLCV data for each
      4. Scores them across 5 strategies: momentum, swing, long_term, breakout, mean_reversion
      5. Returns them ranked by score for the requested trading style

    Args:
        trading_style: "momentum", "swing", "long_term", "breakout", "mean_reversion", or "all"
                       (default "all" ranks by best overall score across strategies)
        top_n: How many stocks to scan (default 20, max 50)
        shariah_only: If True (default), scan only DSES Shariah-compliant stocks.
                      Set False to scan all DSE stocks regardless of Shariah compliance.
    """
    # Shariah-compliant stocks listed on the DSES index
    _SHARIAH_STOCKS = [
        # Islamic Banks
        "ISLAMIBANK", "EXIM", "ALARABANK", "SHAHJALAL", "UNIONBANK",
        # Pharma & Healthcare
        "SQURPHARMA", "RENATA", "ORIONPHAR", "IBNSINA", "ACIPHARM", "BEACONPHAR",
        # Telecom
        "GRAMEENPHONE", "ROBI",
        # Consumer Goods (non-tobacco/alcohol)
        "MARICO", "OLYMPIC", "SINGERBD", "RECKITTBEN",
        # Cement
        "PREMIERCEM", "HEIDELBCEM", "LAFSURCEML", "CONFIDCEM",
        # Steel / Engineering
        "BSRMSTEEL", "BSRMLTD", "GPHISPAT",
        # Power / Energy / Gas
        "KPCL", "SUMITPOWER", "POWERGRID", "DESCO", "TITASGAS", "UPGDCL",
        # Textile
        "SQUARETEX", "APEXFOOT",
        # Diversified / Others
        "ACI", "BERGER", "AFTABAUTO",
    ]

    # All liquid DSE stocks (Shariah and non-Shariah) — fallback when market is closed
    _ALL_LIQUID_STOCKS = [
        "BRACBANK", "GRAMEENPHONE", "BATBC", "SQURPHARMA", "DUTCHBANGLA",
        "RENATA", "ISLAMIBANK", "OLYMPIC", "CITYBANK", "BERGER",
        "BSRMSTEEL", "MARICO", "NCCBANK", "PUBALI", "UCBL",
        "LHBL", "TITASGAS", "POWERGRID", "UPGDCL", "DESCO",
        "BDFINANCE", "DBH", "IFIC", "EBL", "MTBL",
        "KPCL", "SUMITPOWER", "BXPHARMA", "LAFSURCEML",
        "GPHISPAT", "BSRMLTD", "PREMIERCEM", "HEIDELBCEM", "SINGERBD",
        "RECKITTBEN", "APEXFOOT", "SQUARETEX", "BEXIMCO", "AFTABAUTO",
    ]

    top_n = min(int(top_n), 50)
    style = trading_style.lower().strip()
    valid_styles = ("momentum", "swing", "long_term", "breakout", "mean_reversion", "all")
    if style not in valid_styles:
        return _json({"error": f"Invalid style. Choose from: {valid_styles}"})

    shariah_set = set(_SHARIAH_STOCKS)

    # Try live prices first (works during market hours)
    all_prices = dse.get_all_live_prices()
    market_open = bool(all_prices and not (len(all_prices) == 1 and "error" in all_prices[0]))

    if market_open:
        candidates = [s for s in all_prices if s.get("volume") and s.get("symbol")]
        if shariah_only:
            candidates = [s for s in candidates if s.get("symbol", "").strip().upper() in shariah_set]
        active_symbols = [
            {"symbol": s.get("symbol", "").strip(),
             "last_price": s.get("last_price"),
             "change": s.get("change"),
             "volume": s.get("volume")}
            for s in sorted(candidates, key=lambda x: x.get("volume", 0), reverse=True)[:top_n]
        ]
        data_source = "live" + (" — Shariah (DSES) stocks only" if shariah_only else " — all DSE stocks")
    else:
        # Market closed — use known stock lists
        fallback = _SHARIAH_STOCKS if shariah_only else _ALL_LIQUID_STOCKS
        active_symbols = [
            {"symbol": sym, "last_price": None, "change": None, "volume": None}
            for sym in fallback[:top_n]
        ]
        label = "Shariah (DSES)" if shariah_only else "all DSE"
        data_source = f"historical (market closed — {label} stocks, last trading session)"

    results = []
    errors = []

    for stock in active_symbols:
        symbol = stock.get("symbol", "").strip()
        if not symbol:
            continue
        try:
            start, end = dse.default_date_range(90)
            df = dse.get_historical_data(symbol, start, end)
            if df.empty or len(df) < 30:
                continue
            score = ta_lib.score_stock(df)
            if score is None:
                continue
            score["symbol"] = symbol
            # Use last close from history if live price not available
            score["live_price"] = stock.get("last_price") or round(float(df["close"].iloc[-1]), 2)
            score["change_pct"] = stock.get("change")
            score["volume"] = stock.get("volume") or int(df["volume"].iloc[-1])
            score["last_session_date"] = str(df.index[-1].date())
            results.append(score)
        except Exception as e:
            errors.append({"symbol": symbol, "error": str(e)})

    if not results:
        return _json({"error": "No data available for any stock.", "fetch_errors": errors[:5]})

    # Sort by the requested style score
    if style == "all":
        results.sort(key=lambda x: x["best_score"], reverse=True)
        sort_key = "best_score"
    else:
        results.sort(key=lambda x: x["scores"].get(style, 0), reverse=True)
        sort_key = f"scores.{style}"

    # Build a clean ranked output
    ranked = []
    for i, r in enumerate(results, 1):
        style_score = r["scores"].get(style, r["best_score"]) if style != "all" else r["best_score"]
        tp = r.get("trade_plan", {})
        ranked.append({
            "rank": i,
            "symbol": r["symbol"],
            "verdict": r["verdict"],
            "rating": r["rating"],
            "score": style_score,
            "best_strategy": r["best_strategy"],
            "scores": r["scores"],
            "live_price": r["live_price"],
            "change_pct": r["change_pct"],
            "trade_plan": {
                "entry": tp.get("entry"),
                "stop_loss": tp.get("stop_loss"),
                "target_1": tp.get("target_1"),
                "target_2": tp.get("target_2"),
                "risk_pct": tp.get("risk_pct"),
                "risk_reward_t1": tp.get("risk_reward_t1"),
                "risk_reward_t2": tp.get("risk_reward_t2"),
                "note": tp.get("note"),
            },
            "indicators": {
                "rsi": r["rsi"],
                "trend": r["trend"],
                "macd": r["macd"],
                "bb": r["bb"],
                "obv": r["obv"],
            },
        })

    buys = [r for r in ranked if r["verdict"] == "BUY"]
    watches = [r for r in ranked if r["verdict"] == "WATCH"]
    avoids = [r for r in ranked if r["verdict"] == "AVOID"]

    return _json({
        "scan_style": style,
        "shariah_only": shariah_only,
        "data_source": data_source,
        "stocks_scanned": len(results),
        "sort_by": sort_key,
        "summary": {
            "BUY_candidates": len(buys),
            "WATCH_candidates": len(watches),
            "AVOID_count": len(avoids),
            "how_to_read": (
                "trade_plan.entry = suggested entry price | "
                "trade_plan.stop_loss = cut-loss level | "
                "trade_plan.target_1 = first profit target | "
                "trade_plan.target_2 = full target | "
                "risk_reward_t2 e.g. 1:3 means risk 1 taka to make 3"
            ),
        },
        "top_buys": buys[:10],
        "top_watches": watches[:5],
        "full_ranked_list": ranked,
        "fetch_errors": errors[:3] if errors else [],
    })


if __name__ == "__main__":
    mcp.run()
