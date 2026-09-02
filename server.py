#!/usr/bin/env python3
"""
DSE Analysis MCP Server — HTTP + Stdio transport.

Run with:
  python3 server.py --transport http --host 0.0.0.0 --port 8765
  python3 server.py --transport stdio  (for local clients)
"""
import json
import argparse

from mcp.server.fastmcp import FastMCP
import uvicorn
from starlette.routing import Route
from starlette.responses import JSONResponse

import dse_data as dse
import technical_analysis as ta_lib

mcp = FastMCP("DSE Analysis")

_PROJECT_DIR = __import__("os").path.dirname(__import__("os").path.abspath(__file__))

# Store the app reference for later route addition
_app_instance = None

# ---------------------------------------------------------------------------
# Shariah-compliant DSE stocks — merged from two official sources:
#   1. IBSL (Islami Bank Securities Ltd) Shariah Tradeable Stock List — 284 equities
#   2. DSES (DSE Shariah Index) TradingView components — adds CLICL
# Tickers are actual DSE trading codes (corrected where TradingView names differ).
# Last verified: June 2026
# ---------------------------------------------------------------------------
_SHARIAH_STOCKS = {
    # Banks (Islamic)
    "ALARABANK", "EXIMBANK", "FIRSTSBANK", "GIB", "ICBIBANK", "ISLAMIBANK",
    "SHAHJABANK", "SIBL", "STANDBANKL", "UNIONBANK",
    # Insurance
    "FAREASTLIF", "ICICL", "ISLAMIINS", "MERCINS", "NORTHRNINS", "PADMALIFE",
    "PRIMEINSUR", "PRIMELIFE", "SONALILIFE", "TAKAFULINS", "TILIL",
    # Financial Institution
    "ISLAMICFIN",
    # Cement
    "ARAMITCEM", "CONFIDCEM", "CROWNCEMNT", "HEIDELBCEM", "LHBL", "MEGHNACEM", "PREMIERCEM",
    # Ceramics
    "FUWANGCER", "MONNOCERA", "RAKCERAMIC", "SPCERAMICS", "STANCERAM",
    # Engineering
    "AFTABAUTO", "ANWARGALV", "APOLOISPAT", "ATLASBANG", "AZIZPIPES", "BBS", "BBSCABLES",
    "BDAUTOCA", "BDLAMPS", "BDTHAI", "BENGALWTL", "BSRMLTD", "BSRMSTEEL", "COPPERTECH",
    "DESHBANDHU", "DOMINAGE", "ECABLES", "GOLDENSON", "GPHISPAT", "IFADAUTOS", "KAY&QUE",
    "KDSALTD", "MIRAKHTER", "MONNOAGML", "NAHEEACP", "NAVANACNG", "NPOLYMER", "NTLTUBES",
    "OAL", "OIMEX", "QUASEMIND", "RANFOUNDRY", "RENWICKJA", "RSRMSTEEL", "RUNNERAUTO",
    "SALAMCRST", "SHURWID", "SINGERBD", "SSSTEEL", "WALTONHIL", "WMSHIPYARD", "YPL",
    # Food & Allied
    "AMCL(PRAN)", "APEXFOODS", "BANGAS", "BDTHAIFOOD", "BEACHHATCH", "EMERALDOIL",
    "FINEFOODS", "FUWANGFOOD", "GEMINISEA", "GHAIL", "LOVELLO", "MEGCONMILK", "MEGHNAPET",
    "NTC", "OLYMPIC", "RAHIMAFOOD", "RDFOOD", "SHYAMPSUG", "UNILEVERCL", "ZEALBANGLA",
    # Fuel & Power
    "AOL", "BARKAPOWER", "BDWELDING", "BPPL", "CVOPRL", "DESCO", "DOREENPWR", "EASTRNLUB",
    "EPGL", "GBBPOWER", "INTRACO", "JAMUNAOIL", "KPCL", "LINDEBD", "LRBDL", "MJLBD",
    "MPETROLEUM", "PADMAOIL", "POWERGRID", "SPCL", "SUMITPOWER", "TITASGAS", "UPGDCL",
    # IT Sector
    "AAMRANET", "AAMRATECH", "ADNTEL", "AGNISYSL", "BDCOM", "DAFODILCOM", "EGEN",
    "GENEXIL", "INTECH", "ISNLTD", "ITC",
    # Paper & Printing
    "BPML", "HAKKANIPUL", "KPPL", "MONOSPOOL", "PAPERPROC", "SONALIPAPR",
    # Pharmaceuticals & Chemicals
    "ACI", "ACIFORMULA", "ACMELAB", "ACMEPL", "ACTIVEFINE", "ADVENT", "AFCAGRO", "AMBEEPHA",
    "ASIATICLAB", "BEACONPHAR", "BXPHARMA", "BXSYNTH", "CENTRALPHL", "FARCHEM", "GHCL",
    "IBNSINA", "IBP", "IMAMBUTTON", "JHRML", "JMISMDL", "KEYACOSMET", "KOHINOOR", "LIBRAINFU",
    "MARICO", "NAVANAPHAR", "ORIONINFU", "ORIONPHARM", "PHARMAID", "RECKITTBEN", "RENATA",
    "SALVOCHEM", "SILCOPHL", "SILVAPHL", "SQURPHARMA", "TECHNODRUG", "WATACHEM",
    # Services
    "EHL", "SAIFPOWER", "SAMORITA", "SAPORTL",
    # Leather & Footwear
    "APEXFOOT", "APEXTANRY", "BATASHOE", "FORTUNE", "LEGACYFOOT", "SAMATALETH",
    # Telecom
    "BSCCL", "GP", "ROBI",
    # Textiles
    "ACFL", "AIL", "ALIF", "ALLTEX", "ANLIMAYARN", "APEXSPINN", "ARGONDENIM", "CNATEX",
    "DACCADYE", "DELTASPINN", "DSHGARME", "DSSL", "DULAMIACOT", "ENVOYTEX", "ESQUIRENIT",
    "ETL", "FAMILYTEX", "FEKDIL", "GENNEXT", "HFL", "HRTEX", "HWAWELLTEX", "KTL",
    "MAKSONSPIN", "MALEKSPIN", "MATINSPINN", "METROSPIN", "MHSML", "MITHUNKNIT", "MLDYEING",
    "MONNOFABR", "NEWLINE", "NURANI", "PDL", "PRIMETEX", "PTL", "QUEENSOUTH", "RAHIMTEXT",
    "REGENTTEX", "RINGSHINE", "RNSPIN", "SAFKOSPINN", "SAIHAMCOT", "SAIHAMTEX", "SHASHADNIM",
    "SHEPHERD", "SIMTEX", "SONARGAON", "SQUARETEXT", "STYLECRAFT", "TALLUSPIN", "TAMIJTEX",
    "TOSRIFA", "TUNGHAI", "VFSTDL", "ZAHEENSPIN", "ZAHINTEX",
    # Travel & Leisure
    "BDSERVICE", "BESTHLDNG", "PENINSULA", "SEAPEARL", "UNIQUEHRL",
    # Jute
    "JUTESPINN", "NORTHERN", "SONALIANSH",
    # Miscellaneous
    "AMANFEED", "ARAMIT", "BERGERPBL", "BEXIMCO", "BSC", "GQBALLPEN", "HAMI", "INDEXAGRO",
    "KBPPWBIL", "MIRACLEIND", "NFML", "SAVAREFR", "SINOBANGLA", "SKTRIMS", "USMANIAGL",
    "MOSTFAMETL", "NIALCO", "WONDERTOYS",
    # Other/Various
    "ACHIASF", "AOPLC", "BENGALBISC", "YUSUFLOUR", "AMPL", "BDPAINTS", "MAMUNAGRO",
    "SADHESIVE", "APEXWEAV", "HIMADRI", "KBSEED", "KFL", "MASTERAGRO", "ORYZAAGRO",
    "CRAFTSMAN", "MKFOOTWEAR", "WEBCOATS",
    # From DSES index — confirmed Shariah, not in IBSL list
    "CLICL",
}


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
      1. Fetches live prices for all ~396 DSE stocks by volume
      2. If shariah_only=True (default), excludes known non-Shariah stocks (conventional
         banks, tobacco) — all others are treated as potentially Shariah-compliant
      3. Downloads 90 days of OHLCV data for each
      4. Scores them across 5 strategies: momentum, swing, long_term, breakout, mean_reversion
      5. Returns them ranked by score for the requested trading style

    Args:
        trading_style: "momentum", "swing", "long_term", "breakout", "mean_reversion", or "all"
                       (default "all" ranks by best overall score across strategies)
        top_n: How many stocks to scan (default 20, max 50)
        shariah_only: If True (default), exclude known non-Shariah stocks (conventional
                      banks, tobacco). Set False to scan all DSE stocks.
    """
    top_n = min(int(top_n), 50)
    style = trading_style.lower().strip()
    valid_styles = ("momentum", "swing", "long_term", "breakout", "mean_reversion", "all")
    if style not in valid_styles:
        return _json({"error": f"Invalid style. Choose from: {valid_styles}"})

    # Try live prices first (works during market hours) — covers all ~396 DSE stocks
    all_prices = dse.get_all_live_prices()
    market_open = bool(all_prices and not (len(all_prices) == 1 and "error" in all_prices[0]))

    if market_open:
        candidates = [s for s in all_prices if s.get("volume") and s.get("symbol")]
        if shariah_only:
            candidates = [s for s in candidates
                          if s.get("symbol", "").strip().upper() in _SHARIAH_STOCKS]
        active_symbols = [
            {"symbol": s.get("symbol", "").strip(),
             "last_price": s.get("last_price"),
             "change": s.get("change"),
             "volume": s.get("volume")}
            for s in sorted(candidates, key=lambda x: x.get("volume", 0), reverse=True)[:top_n]
        ]
        label = "IBSL/DSES Shariah stocks" if shariah_only else "all DSE stocks"
        data_source = f"live — {label}"
    else:
        # Market closed — use Shariah stock list directly
        if shariah_only:
            fallback = sorted(_SHARIAH_STOCKS)
        else:
            fallback = sorted(_SHARIAH_STOCKS) + [
                "BRACBANK", "DUTCHBANGLA", "CITYBANK", "PUBALI", "NCCBANK",
                "EBL", "MTBL", "UCBL", "IFIC", "BATBC",
            ]
        seen = set()
        fallback = [s for s in fallback if not (s in seen or seen.add(s))]
        active_symbols = [
            {"symbol": sym, "last_price": None, "change": None, "volume": None}
            for sym in fallback[:top_n]
        ]
        label = "IBSL/DSES Shariah" if shariah_only else "all DSE"
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


@mcp.tool()
def get_engulfing_pattern(symbol: str, lookback: int = 5, days: int = 90) -> str:
    """
    Detect bullish or bearish engulfing candlestick patterns for a single DSE stock.
    Returns the most recent engulfing pattern found within the lookback window,
    with strength rating, volume confirmation, RSI context, and interpretation.

    Args:
        symbol: DSE trading code, e.g. SQURPHARMA, ISLAMIBANK
        lookback: How many recent candles to scan for the pattern (default 5)
        days: Historical data to load (default 90)
    """
    df, err = _load_history(symbol, days)
    if err:
        return _json({"error": err})
    result = ta_lib.detect_engulfing(df, lookback=lookback)
    result["symbol"] = symbol.upper()
    return _json(result)


@mcp.tool()
def scan_engulfing_stocks(
    pattern: str = "both",
    lookback: int = 3,
    shariah_only: bool = True,
    top_n: int = 30,
) -> str:
    """
    Scan DSE stocks for recent bullish or bearish engulfing candlestick patterns.
    Returns a ranked list — strongest patterns (by body ratio + volume) first.

    Args:
        pattern: "bullish" — only bullish engulfing (reversal up)
                 "bearish" — only bearish engulfing (reversal down)
                 "both"    — all engulfing patterns (default)
        lookback: Candles to look back for the pattern per stock (default 3 = last 3 sessions)
        shariah_only: If True (default), exclude known non-Shariah stocks (conventional
                      banks, tobacco). Set False to scan all DSE stocks.
        top_n: Number of stocks to scan (default 30, max 50)
    """
    top_n = min(int(top_n), 50)
    pattern = pattern.lower().strip()
    if pattern not in ("bullish", "bearish", "both"):
        return _json({"error": "pattern must be 'bullish', 'bearish', or 'both'"})

    # Try to enrich with live prices and build stock list from all DSE stocks
    all_prices = dse.get_all_live_prices()
    price_map = {}
    market_open = bool(all_prices and not (len(all_prices) == 1 and "error" in all_prices[0]))

    if market_open:
        candidates = [s for s in all_prices if s.get("volume") and s.get("symbol")]
        if shariah_only:
            candidates = [s for s in candidates
                          if s.get("symbol", "").strip().upper() in _SHARIAH_STOCKS]
        for s in candidates:
            sym = s.get("symbol", "").strip().upper()
            if sym:
                price_map[sym] = {
                    "live_price": s.get("last_price"),
                    "change_pct": s.get("change"),
                    "volume": s.get("volume"),
                }
        stock_list = [s.get("symbol", "").strip() for s in
                      sorted(candidates, key=lambda x: x.get("volume", 0), reverse=True)][:top_n]
    else:
        if shariah_only:
            fallback = sorted(_SHARIAH_STOCKS)
        else:
            fallback = sorted(_SHARIAH_STOCKS) + [
                "BRACBANK", "DUTCHBANGLA", "CITYBANK", "PUBALI", "NCCBANK",
                "EBL", "MTBL", "UCBL", "IFIC", "BATBC",
            ]
        seen = set()
        stock_list = [s for s in fallback if not (s in seen or seen.add(s))][:top_n]

    found = []
    errors = []

    for symbol in stock_list:
        try:
            start, end = dse.default_date_range(90)
            df = dse.get_historical_data(symbol, start, end)
            if df.empty or len(df) < 20:
                continue
            result = ta_lib.detect_engulfing(df, lookback=lookback)
            if result.get("pattern") == "NONE":
                continue
            pat = result["pattern"]
            if pattern == "bullish" and "BULLISH" not in pat:
                continue
            if pattern == "bearish" and "BEARISH" not in pat:
                continue

            live = price_map.get(symbol, {})
            found.append({
                "symbol": symbol,
                "pattern": pat,
                "signal": result["signal"],
                "strength": result["strength"],
                "candle_when": result.get("candle_index", "recent"),
                "body_ratio": result["body_ratio"],
                "volume_ratio": result["volume_ratio"],
                "volume_confirmed": result["volume_confirmed"],
                "rsi_at_signal": result["rsi_at_signal"],
                "rsi_context": result["rsi_context"],
                "prev_candle": result["prev_candle"],
                "curr_candle": result["curr_candle"],
                "interpretation": result["interpretation"],
                "live_price": live.get("live_price") or round(float(df["close"].iloc[-1]), 2),
                "change_pct": live.get("change_pct"),
            })
        except Exception as e:
            errors.append({"symbol": symbol, "error": str(e)})

    if not found:
        return _json({
            "pattern_filter": pattern,
            "shariah_only": shariah_only,
            "stocks_scanned": len(stock_list),
            "result": "No engulfing patterns found in the last {} sessions".format(lookback),
            "fetch_errors": errors[:3],
        })

    # Sort: STRONG first, then by body_ratio desc, then volume_ratio desc
    strength_order = {"STRONG": 0, "MODERATE": 1, "WEAK": 2}
    found.sort(key=lambda x: (strength_order.get(x["strength"], 9), -x["body_ratio"], -x["volume_ratio"]))

    bullish_list = [r for r in found if "BULLISH" in r["pattern"]]
    bearish_list = [r for r in found if "BEARISH" in r["pattern"]]

    return _json({
        "pattern_filter": pattern,
        "shariah_only": shariah_only,
        "stocks_scanned": len(stock_list),
        "lookback_sessions": lookback,
        "total_found": len(found),
        "bullish_engulfing_count": len(bullish_list),
        "bearish_engulfing_count": len(bearish_list),
        "how_to_read": (
            "strength: STRONG = big body + volume spike | MODERATE = one of the two | WEAK = pattern only. "
            "body_ratio: how many times larger the engulfing candle's body is vs the prior candle. "
            "volume_ratio: engulfing candle volume vs 20-day average."
        ),
        "bullish_engulfing": bullish_list,
        "bearish_engulfing": bearish_list,
        "all_results": found,
        "fetch_errors": errors[:3] if errors else [],
    })


def main():
    parser = argparse.ArgumentParser(description="DSE Analysis MCP Server")
    parser.add_argument(
        "--transport",
        choices=["http", "stdio"],
        default="stdio",
        help="Transport mode (http for remote, stdio for local clients)",
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to (HTTP mode only)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="Port to listen on (HTTP mode only)",
    )
    
    args = parser.parse_args()
    
    if args.transport == "http":
        print(f"Starting DSE Analysis MCP Server on http://{args.host}:{args.port}")
        print(f"Connect clients to: http://{args.host}:{args.port}")
        print(f"Documentation available at: http://{args.host}:{args.port}/docs")
        app = mcp.streamable_http_app()
        
        # Add health check endpoint using Starlette routing
        async def health_check(request):
            return JSONResponse({
                "status": "ok",
                "service": "DSE Analysis MCP Server",
                "version": "1.0",
                "docs": "/docs",
                "openapi": "/openapi.json"
            })
        
        # Add OAuth protected resource metadata endpoint (RFC 9728 compliance)
        # This endpoint must return the correct resource URL that matches the MCP server endpoint
        async def oauth_protected_resource_metadata(request):
            # Get the scheme and host from the request
            scheme = request.url.scheme
            host = request.url.netloc
            # Return metadata with resource pointing to the MCP endpoint
            return JSONResponse({
                "resource": f"{scheme}://{host}/mcp",
                "authorization_servers": [],
                "scopes_supported": [],
                "bearer_methods_supported": ["header"]
            })
        
        # Add the routes to the app
        app.routes.append(Route("/", health_check, methods=["GET"]))
        app.routes.append(Route("/.well-known/oauth-protected-resource", oauth_protected_resource_metadata, methods=["GET"]))
        
        uvicorn.run(
            app,
            host=args.host,
            port=args.port,
            log_level="info",
        )
    else:
        # Stdio mode (default)
        mcp.run()


if __name__ == "__main__":
    main()
