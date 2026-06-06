"""World-famous technical analysis indicators using pandas-ta."""
import numpy as np
import pandas as pd

HAS_PANDAS_TA = False


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _require_ohlcv(df: pd.DataFrame) -> str | None:
    needed = {"open", "high", "low", "close", "volume"}
    missing = needed - set(df.columns)
    if missing:
        return f"Missing columns: {missing}"
    if len(df) < 30:
        return "Need at least 30 candles for analysis"
    return None


def _signal(condition_buy: bool, condition_sell: bool) -> str:
    if condition_buy:
        return "BUY"
    if condition_sell:
        return "SELL"
    return "NEUTRAL"


# ---------------------------------------------------------------------------
# Moving Averages & Trend
# ---------------------------------------------------------------------------

def analyze_trend(df: pd.DataFrame) -> dict:
    err = _require_ohlcv(df)
    if err:
        return {"error": err}

    close = df["close"]
    results = {}

    # SMA
    for period in [20, 50, 200]:
        if len(close) >= period:
            sma = close.rolling(period).mean()
            results[f"SMA_{period}"] = round(sma.iloc[-1], 2)

    # EMA
    for period in [9, 21, 55]:
        ema = close.ewm(span=period, adjust=False).mean()
        results[f"EMA_{period}"] = round(ema.iloc[-1], 2)

    price = round(close.iloc[-1], 2)
    results["current_price"] = price

    # Trend direction
    sma20 = results.get("SMA_20")
    sma50 = results.get("SMA_50")
    sma200 = results.get("SMA_200")
    ema9 = results.get("EMA_9")
    ema21 = results.get("EMA_21")

    signals = []
    if sma50 and sma200:
        if sma50 > sma200:
            signals.append("GOLDEN CROSS (bullish)")
        else:
            signals.append("DEATH CROSS (bearish)")

    if sma20 and price > sma20:
        signals.append(f"Price above SMA20 (bullish)")
    elif sma20:
        signals.append(f"Price below SMA20 (bearish)")

    if ema9 and ema21:
        if ema9 > ema21:
            signals.append("EMA9 > EMA21 (short-term bullish)")
        else:
            signals.append("EMA9 < EMA21 (short-term bearish)")

    # Overall trend
    bullish_count = sum(1 for s in signals if "bullish" in s)
    bearish_count = sum(1 for s in signals if "bearish" in s)
    if bullish_count > bearish_count:
        results["trend"] = "UPTREND"
    elif bearish_count > bullish_count:
        results["trend"] = "DOWNTREND"
    else:
        results["trend"] = "SIDEWAYS"

    results["signals"] = signals
    return results


# ---------------------------------------------------------------------------
# Momentum
# ---------------------------------------------------------------------------

def _rsi_manual(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def analyze_momentum(df: pd.DataFrame) -> dict:
    err = _require_ohlcv(df)
    if err:
        return {"error": err}

    close = df["close"]
    high = df["high"]
    low = df["low"]
    results = {}

    # --- RSI ---
    if HAS_PANDAS_TA:
        rsi_series = df.ta.rsi(length=14)
    else:
        rsi_series = _rsi_manual(close, 14)

    rsi = round(float(rsi_series.iloc[-1]), 2)
    results["RSI_14"] = rsi
    if rsi >= 70:
        results["RSI_signal"] = "OVERBOUGHT — potential reversal down"
    elif rsi <= 30:
        results["RSI_signal"] = "OVERSOLD — potential reversal up"
    elif rsi >= 60:
        results["RSI_signal"] = "BULLISH momentum"
    elif rsi <= 40:
        results["RSI_signal"] = "BEARISH momentum"
    else:
        results["RSI_signal"] = "NEUTRAL"

    # --- MACD (12, 26, 9) ---
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    histogram = macd_line - signal_line

    results["MACD_line"] = round(float(macd_line.iloc[-1]), 4)
    results["MACD_signal"] = round(float(signal_line.iloc[-1]), 4)
    results["MACD_histogram"] = round(float(histogram.iloc[-1]), 4)

    # MACD crossover signal
    if macd_line.iloc[-1] > signal_line.iloc[-1] and macd_line.iloc[-2] <= signal_line.iloc[-2]:
        results["MACD_crossover"] = "BULLISH crossover (buy signal)"
    elif macd_line.iloc[-1] < signal_line.iloc[-1] and macd_line.iloc[-2] >= signal_line.iloc[-2]:
        results["MACD_crossover"] = "BEARISH crossover (sell signal)"
    elif macd_line.iloc[-1] > signal_line.iloc[-1]:
        results["MACD_crossover"] = "MACD above signal (bullish)"
    else:
        results["MACD_crossover"] = "MACD below signal (bearish)"

    # Divergence check (last 20 candles)
    if len(close) >= 20:
        price_trend = close.iloc[-1] > close.iloc[-20]
        macd_trend = macd_line.iloc[-1] > macd_line.iloc[-20]
        if price_trend and not macd_trend:
            results["MACD_divergence"] = "BEARISH divergence — price up but MACD down"
        elif not price_trend and macd_trend:
            results["MACD_divergence"] = "BULLISH divergence — price down but MACD up"

    # --- Stochastic (14, 3, 3) ---
    if len(df) >= 14:
        low14 = low.rolling(14).min()
        high14 = high.rolling(14).max()
        k = 100 * (close - low14) / (high14 - low14 + 1e-9)
        d = k.rolling(3).mean()
        k_val = round(float(k.iloc[-1]), 2)
        d_val = round(float(d.iloc[-1]), 2)
        results["Stoch_%K"] = k_val
        results["Stoch_%D"] = d_val
        if k_val >= 80:
            results["Stoch_signal"] = "OVERBOUGHT"
        elif k_val <= 20:
            results["Stoch_signal"] = "OVERSOLD"
        elif k.iloc[-1] > d.iloc[-1] and k.iloc[-2] <= d.iloc[-2]:
            results["Stoch_signal"] = "BULLISH crossover"
        elif k.iloc[-1] < d.iloc[-1] and k.iloc[-2] >= d.iloc[-2]:
            results["Stoch_signal"] = "BEARISH crossover"
        else:
            results["Stoch_signal"] = "NEUTRAL"

    # --- Williams %R ---
    if len(df) >= 14:
        highest_high = high.rolling(14).max()
        lowest_low = low.rolling(14).min()
        wr = -100 * (highest_high - close) / (highest_high - lowest_low + 1e-9)
        results["Williams_%R"] = round(float(wr.iloc[-1]), 2)
        results["Williams_signal"] = "OVERBOUGHT" if wr.iloc[-1] >= -20 else ("OVERSOLD" if wr.iloc[-1] <= -80 else "NEUTRAL")

    # --- Rate of Change ---
    if len(close) >= 12:
        roc = ((close - close.shift(12)) / close.shift(12)) * 100
        results["ROC_12"] = round(float(roc.iloc[-1]), 2)

    # Overall momentum signal
    buy_signals = sum(1 for k, v in results.items()
                      if isinstance(v, str) and ("BUY" in v.upper() or "BULLISH" in v.upper() or "OVERSOLD" in v.upper()))
    sell_signals = sum(1 for k, v in results.items()
                       if isinstance(v, str) and ("SELL" in v.upper() or "BEARISH" in v.upper() or "OVERBOUGHT" in v.upper()))
    results["momentum_verdict"] = "BULLISH" if buy_signals > sell_signals else ("BEARISH" if sell_signals > buy_signals else "NEUTRAL")

    return results


# ---------------------------------------------------------------------------
# Volatility
# ---------------------------------------------------------------------------

def analyze_volatility(df: pd.DataFrame) -> dict:
    err = _require_ohlcv(df)
    if err:
        return {"error": err}

    close = df["close"]
    high = df["high"]
    low = df["low"]
    results = {}

    # --- Bollinger Bands (20, 2) ---
    sma20 = close.rolling(20).mean()
    std20 = close.rolling(20).std()
    upper_band = sma20 + 2 * std20
    lower_band = sma20 - 2 * std20
    bb_width = (upper_band - lower_band) / sma20 * 100

    price = close.iloc[-1]
    results["BB_upper"] = round(float(upper_band.iloc[-1]), 2)
    results["BB_middle"] = round(float(sma20.iloc[-1]), 2)
    results["BB_lower"] = round(float(lower_band.iloc[-1]), 2)
    results["BB_width_pct"] = round(float(bb_width.iloc[-1]), 2)

    # BB signal
    if price >= upper_band.iloc[-1]:
        results["BB_signal"] = "Price at UPPER band — overbought / breakout"
    elif price <= lower_band.iloc[-1]:
        results["BB_signal"] = "Price at LOWER band — oversold / breakdown"
    elif bb_width.iloc[-1] < bb_width.rolling(20).mean().iloc[-1] * 0.7:
        results["BB_signal"] = "SQUEEZE detected — big move incoming"
    else:
        results["BB_signal"] = "Price within bands — normal range"

    # BB %B (position within bands)
    percent_b = (price - lower_band.iloc[-1]) / (upper_band.iloc[-1] - lower_band.iloc[-1] + 1e-9)
    results["BB_percent_B"] = round(float(percent_b), 3)

    # --- ATR (14) ---
    tr = pd.concat([
        high - low,
        (high - close.shift(1)).abs(),
        (low - close.shift(1)).abs(),
    ], axis=1).max(axis=1)
    atr = tr.ewm(span=14, adjust=False).mean()
    results["ATR_14"] = round(float(atr.iloc[-1]), 2)
    results["ATR_pct_of_price"] = round(float(atr.iloc[-1] / price * 100), 2)
    results["suggested_stop_loss"] = round(float(price - 2 * atr.iloc[-1]), 2)
    results["suggested_target"] = round(float(price + 3 * atr.iloc[-1]), 2)

    # --- Historical Volatility (20-day annualized) ---
    log_returns = np.log(close / close.shift(1)).dropna()
    if len(log_returns) >= 20:
        hv = float(log_returns.rolling(20).std().iloc[-1]) * np.sqrt(252) * 100
        results["historical_volatility_pct"] = round(hv, 2)
        if hv > 60:
            results["volatility_level"] = "HIGH"
        elif hv > 30:
            results["volatility_level"] = "MODERATE"
        else:
            results["volatility_level"] = "LOW"

    return results


# ---------------------------------------------------------------------------
# Volume
# ---------------------------------------------------------------------------

def analyze_volume(df: pd.DataFrame) -> dict:
    err = _require_ohlcv(df)
    if err:
        return {"error": err}

    close = df["close"]
    volume = df["volume"]
    results = {}

    # --- OBV (On-Balance Volume) ---
    price_diff = close.diff()
    obv = (np.where(price_diff > 0, volume, np.where(price_diff < 0, -volume, 0))).cumsum()
    obv_series = pd.Series(obv, index=df.index)
    results["OBV_current"] = int(obv_series.iloc[-1])

    # OBV trend vs price trend
    if len(obv_series) >= 20:
        obv_trend_up = obv_series.iloc[-1] > obv_series.iloc[-20]
        price_trend_up = close.iloc[-1] > close.iloc[-20]
        if price_trend_up and obv_trend_up:
            results["OBV_signal"] = "CONFIRMED UPTREND — price and volume both rising"
        elif price_trend_up and not obv_trend_up:
            results["OBV_signal"] = "BEARISH DIVERGENCE — price up but volume declining"
        elif not price_trend_up and obv_trend_up:
            results["OBV_signal"] = "BULLISH DIVERGENCE — price down but accumulation occurring"
        else:
            results["OBV_signal"] = "CONFIRMED DOWNTREND — price and volume declining"

    # --- Volume Moving Average ---
    vol_ma20 = volume.rolling(20).mean()
    results["volume_current"] = int(volume.iloc[-1])
    results["volume_MA20"] = int(vol_ma20.iloc[-1])
    vol_ratio = volume.iloc[-1] / vol_ma20.iloc[-1]
    results["volume_vs_average"] = f"{round(float(vol_ratio), 2)}x average"
    if vol_ratio >= 2.0:
        results["volume_signal"] = "HIGH VOLUME — strong conviction move"
    elif vol_ratio >= 1.5:
        results["volume_signal"] = "ABOVE AVERAGE volume"
    elif vol_ratio <= 0.5:
        results["volume_signal"] = "LOW VOLUME — weak conviction"
    else:
        results["volume_signal"] = "NORMAL volume"

    # --- VWAP (rolling, last 20 periods) ---
    if len(df) >= 20:
        typical_price = (df["high"] + df["low"] + close) / 3
        vwap_num = (typical_price * volume).rolling(20).sum()
        vwap_den = volume.rolling(20).sum()
        vwap = vwap_num / vwap_den
        results["VWAP_20"] = round(float(vwap.iloc[-1]), 2)
        if close.iloc[-1] > vwap.iloc[-1]:
            results["VWAP_signal"] = "Price above VWAP — bullish bias"
        else:
            results["VWAP_signal"] = "Price below VWAP — bearish bias"

    return results


# ---------------------------------------------------------------------------
# Fibonacci Levels
# ---------------------------------------------------------------------------

def fibonacci_levels(df: pd.DataFrame, lookback: int = 60) -> dict:
    if df.empty or len(df) < 5:
        return {"error": "Insufficient data for Fibonacci analysis"}

    window = df.tail(lookback)
    swing_high = float(window["high"].max())
    swing_low = float(window["low"].min())
    price = float(df["close"].iloc[-1])
    diff = swing_high - swing_low

    ratios = {
        "0%": swing_high,
        "23.6%": swing_high - 0.236 * diff,
        "38.2%": swing_high - 0.382 * diff,
        "50%": swing_high - 0.500 * diff,
        "61.8%": swing_high - 0.618 * diff,
        "78.6%": swing_high - 0.786 * diff,
        "100%": swing_low,
    }
    extensions = {
        "127.2%": swing_low - 0.272 * diff,
        "161.8%": swing_low - 0.618 * diff,
        "261.8%": swing_low - 1.618 * diff,
    }

    # Find nearest support and resistance
    levels = sorted(ratios.values())
    support = max((l for l in levels if l <= price), default=None)
    resistance = min((l for l in levels if l > price), default=None)

    # Determine which Fibonacci zone price is in
    zone = None
    for name, level in sorted(ratios.items(), key=lambda x: x[1], reverse=True):
        if price <= level:
            zone = name
    if zone is None:
        zone = "Below all levels"

    return {
        "swing_high": round(swing_high, 2),
        "swing_low": round(swing_low, 2),
        "current_price": round(price, 2),
        "retracements": {k: round(v, 2) for k, v in ratios.items()},
        "extensions": {k: round(v, 2) for k, v in extensions.items()},
        "nearest_support": round(support, 2) if support else None,
        "nearest_resistance": round(resistance, 2) if resistance else None,
        "current_fib_zone": zone,
        "signal": (
            "Near strong SUPPORT (61.8%) — consider buying" if zone == "61.8%" else
            "Near strong SUPPORT (38.2%) — watch for bounce" if zone == "38.2%" else
            "Near RESISTANCE — consider taking profits" if zone in ("23.6%", "0%") else
            "Mid-range — watch key levels"
        ),
    }


# ---------------------------------------------------------------------------
# Ichimoku Cloud
# ---------------------------------------------------------------------------

def ichimoku_cloud(df: pd.DataFrame) -> dict:
    if len(df) < 52:
        return {"error": "Need at least 52 candles for Ichimoku analysis"}

    high = df["high"]
    low = df["low"]
    close = df["close"]

    # Tenkan-sen (Conversion Line): (9-period high + 9-period low) / 2
    tenkan = (high.rolling(9).max() + low.rolling(9).min()) / 2

    # Kijun-sen (Base Line): (26-period high + 26-period low) / 2
    kijun = (high.rolling(26).max() + low.rolling(26).min()) / 2

    # Senkou Span A (Leading Span A): (Tenkan + Kijun) / 2, shifted 26 forward
    senkou_a = ((tenkan + kijun) / 2).shift(26)

    # Senkou Span B (Leading Span B): (52-period high + 52-period low) / 2, shifted 26 forward
    senkou_b = ((high.rolling(52).max() + low.rolling(52).min()) / 2).shift(26)

    # Chikou Span: current close vs price 26 periods ago (above = bullish)
    chikou_bullish = (float(close.iloc[-1]) > float(close.iloc[-27])) if len(close) >= 27 else None

    price = float(close.iloc[-1])
    t = float(tenkan.iloc[-1])
    k = float(kijun.iloc[-1])

    # Cloud at current price (use -1 for current, not future)
    cloud_top = max(float(senkou_a.iloc[-1]) if not pd.isna(senkou_a.iloc[-1]) else 0,
                    float(senkou_b.iloc[-1]) if not pd.isna(senkou_b.iloc[-1]) else 0)
    cloud_bottom = min(float(senkou_a.iloc[-1]) if not pd.isna(senkou_a.iloc[-1]) else 0,
                       float(senkou_b.iloc[-1]) if not pd.isna(senkou_b.iloc[-1]) else 0)

    signals = []

    # Price vs Cloud
    if price > cloud_top:
        signals.append("Price ABOVE cloud (bullish)")
        cloud_signal = "BULLISH"
    elif price < cloud_bottom:
        signals.append("Price BELOW cloud (bearish)")
        cloud_signal = "BEARISH"
    else:
        signals.append("Price INSIDE cloud (neutral/consolidation)")
        cloud_signal = "NEUTRAL"

    # TK Cross
    if t > k:
        signals.append("Tenkan above Kijun (bullish TK cross)")
    else:
        signals.append("Tenkan below Kijun (bearish TK cross)")

    # Cloud color (future cloud)
    future_idx = -1
    sa_future = float(senkou_a.iloc[future_idx]) if not pd.isna(senkou_a.iloc[future_idx]) else None
    sb_future = float(senkou_b.iloc[future_idx]) if not pd.isna(senkou_b.iloc[future_idx]) else None
    if sa_future and sb_future:
        cloud_color = "GREEN (bullish)" if sa_future > sb_future else "RED (bearish)"
        signals.append(f"Cloud color: {cloud_color}")
    else:
        cloud_color = "Unknown"

    return {
        "tenkan_sen": round(t, 2),
        "kijun_sen": round(k, 2),
        "senkou_span_A": round(float(senkou_a.iloc[-1]), 2) if not pd.isna(senkou_a.iloc[-1]) else None,
        "senkou_span_B": round(float(senkou_b.iloc[-1]), 2) if not pd.isna(senkou_b.iloc[-1]) else None,
        "cloud_top": round(cloud_top, 2),
        "cloud_bottom": round(cloud_bottom, 2),
        "cloud_color": cloud_color,
        "current_price": round(price, 2),
        "cloud_signal": cloud_signal,
        "chikou_signal": ("Chikou above price 26 periods ago (bullish)" if chikou_bullish
                          else "Chikou below price 26 periods ago (bearish)" if chikou_bullish is not None
                          else "Insufficient data"),
        "signals": signals,
    }


# ---------------------------------------------------------------------------
# Pivot Points
# ---------------------------------------------------------------------------

def pivot_points(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"error": "No data"}
    last = df.iloc[-2] if len(df) >= 2 else df.iloc[-1]
    h = float(last["high"])
    l = float(last["low"])
    c = float(last["close"])
    pivot = (h + l + c) / 3
    r1 = 2 * pivot - l
    r2 = pivot + (h - l)
    r3 = h + 2 * (pivot - l)
    s1 = 2 * pivot - h
    s2 = pivot - (h - l)
    s3 = l - 2 * (h - pivot)
    return {
        "pivot": round(pivot, 2),
        "R1": round(r1, 2), "R2": round(r2, 2), "R3": round(r3, 2),
        "S1": round(s1, 2), "S2": round(s2, 2), "S3": round(s3, 2),
    }


# ---------------------------------------------------------------------------
# Full Analysis Report
# ---------------------------------------------------------------------------

def full_analysis(df: pd.DataFrame, symbol: str = "") -> dict:
    report = {"symbol": symbol}

    trend = analyze_trend(df)
    momentum = analyze_momentum(df)
    volatility = analyze_volatility(df)
    volume = analyze_volume(df)
    fib = fibonacci_levels(df)
    ichimoku = ichimoku_cloud(df)
    pivots = pivot_points(df)

    report["trend_analysis"] = trend
    report["momentum_analysis"] = momentum
    report["volatility_analysis"] = volatility
    report["volume_analysis"] = volume
    report["fibonacci_levels"] = fib
    report["ichimoku_cloud"] = ichimoku
    report["pivot_points"] = pivots

    # Aggregate buy/sell signals
    buy_score = 0
    sell_score = 0

    if trend.get("trend") == "UPTREND":
        buy_score += 2
    elif trend.get("trend") == "DOWNTREND":
        sell_score += 2

    for signal in trend.get("signals", []):
        if "bullish" in signal.lower():
            buy_score += 1
        if "bearish" in signal.lower():
            sell_score += 1

    rsi = momentum.get("RSI_14", 50)
    if rsi <= 30:
        buy_score += 2
    elif rsi >= 70:
        sell_score += 2
    elif rsi < 45:
        sell_score += 1
    elif rsi > 55:
        buy_score += 1

    if "BULLISH" in str(momentum.get("MACD_crossover", "")):
        buy_score += 2
    elif "BEARISH" in str(momentum.get("MACD_crossover", "")):
        sell_score += 2

    if "above VWAP" in str(volume.get("VWAP_signal", "")):
        buy_score += 1
    else:
        sell_score += 1

    cloud_sig = ichimoku.get("cloud_signal", "NEUTRAL")
    if cloud_sig == "BULLISH":
        buy_score += 2
    elif cloud_sig == "BEARISH":
        sell_score += 2

    total = buy_score + sell_score
    if total == 0:
        confidence = 0
    else:
        confidence = round(max(buy_score, sell_score) / total * 100, 1)

    if buy_score > sell_score:
        verdict = "BUY"
    elif sell_score > buy_score:
        verdict = "SELL"
    else:
        verdict = "HOLD/NEUTRAL"

    report["overall_signal"] = {
        "verdict": verdict,
        "confidence_pct": confidence,
        "buy_score": buy_score,
        "sell_score": sell_score,
        "summary": (
            f"{'Strong ' if confidence > 70 else ''}{verdict} signal with {confidence}% confidence. "
            f"Trend: {trend.get('trend', 'N/A')}, RSI: {rsi}, "
            f"MACD: {momentum.get('MACD_crossover', 'N/A')}, "
            f"Ichimoku: {cloud_sig}"
        ),
    }

    return report


# ---------------------------------------------------------------------------
# Strategy Scorer (used by market scanner)
# ---------------------------------------------------------------------------

def score_stock(df: pd.DataFrame) -> dict | None:
    """Score a stock for 5 trading strategies. Returns None if data insufficient."""
    if df is None or df.empty or len(df) < 30:
        return None

    try:
        trend = analyze_trend(df)
        momentum = analyze_momentum(df)
        volatility = analyze_volatility(df)
        volume = analyze_volume(df)
    except Exception:
        return None

    rsi = momentum.get("RSI_14", 50)
    macd_cross = str(momentum.get("MACD_crossover", ""))
    macd_div = str(momentum.get("MACD_divergence", ""))
    bb_signal = str(volatility.get("BB_signal", ""))
    bb_width = volatility.get("BB_width_pct", 99)
    vol_signal = str(volume.get("volume_signal", ""))
    obv_signal = str(volume.get("OBV_signal", ""))
    vwap_signal = str(volume.get("VWAP_signal", ""))
    trend_dir = trend.get("trend", "SIDEWAYS")
    signals = " ".join(trend.get("signals", []))

    # --- Momentum score (0-15) ---
    ms = 0
    if 50 <= rsi <= 70:
        ms += 2
    if "BULLISH" in macd_cross:
        ms += 3
    if trend_dir == "UPTREND":
        ms += 2
    if "HIGH VOLUME" in vol_signal or "ABOVE AVERAGE" in vol_signal:
        ms += 2
    if "above VWAP" in vwap_signal:
        ms += 1
    if "GOLDEN CROSS" in signals:
        ms += 2
    if "CONFIRMED UPTREND" in obv_signal:
        ms += 2
    if "bullish" in signals.lower():
        ms += 1

    # --- Swing score (0-15) ---
    sw = 0
    if 25 <= rsi <= 45:
        sw += 3
    elif rsi < 25:
        sw += 2
    if "LOWER" in bb_signal:
        sw += 3
    if "BULLISH" in macd_div:
        sw += 3
    if "BULLISH DIVERGENCE" in obv_signal:
        sw += 3
    if "SQUEEZE" in bb_signal:
        sw += 1
    if bb_width < 10:
        sw += 2

    # --- Long-term score (0-15) ---
    lt = 0
    if "GOLDEN CROSS" in signals:
        lt += 4
    if trend_dir == "UPTREND":
        lt += 3
    if rsi > 50:
        lt += 1
    if "CONFIRMED UPTREND" in obv_signal:
        lt += 3
    if "BULLISH" in macd_cross:
        lt += 2
    if "bullish" in signals.lower():
        lt += 2

    # --- Breakout score (0-15) ---
    bo = 0
    if "UPPER" in bb_signal:
        bo += 3
    if "HIGH VOLUME" in vol_signal:
        bo += 3
    if 50 <= rsi <= 72:
        bo += 2
    if "BULLISH" in macd_cross:
        bo += 3
    if trend_dir == "UPTREND":
        bo += 2
    if "SQUEEZE" in bb_signal:
        bo += 2

    # --- Mean reversion score (0-15) ---
    mr = 0
    if rsi <= 30:
        mr += 4
    elif rsi <= 35:
        mr += 3
    elif rsi <= 40:
        mr += 2
    if "LOWER" in bb_signal:
        mr += 4
    if "BULLISH DIVERGENCE" in obv_signal:
        mr += 3
    if "OVERSOLD" in str(momentum.get("Stoch_signal", "")):
        mr += 2
    if "BULLISH" in macd_div:
        mr += 2

    scores = {
        "momentum": min(ms, 15),
        "swing": min(sw, 15),
        "long_term": min(lt, 15),
        "breakout": min(bo, 15),
        "mean_reversion": min(mr, 15),
    }
    best_strategy, best_score = max(scores.items(), key=lambda x: x[1])
    stars = "★" * min(5, max(1, round(best_score / 3)))
    verdict = "BUY" if best_score >= 9 else "WATCH" if best_score >= 6 else "AVOID"

    # --- Price targets ---
    price = float(df["close"].iloc[-1])
    tr = pd.concat([
        df["high"] - df["low"],
        (df["high"] - df["close"].shift(1)).abs(),
        (df["low"] - df["close"].shift(1)).abs(),
    ], axis=1).max(axis=1)
    atr = float(tr.ewm(span=14, adjust=False).mean().iloc[-1])
    sma20_val = float(df["close"].rolling(20).mean().iloc[-1])
    std20_val = float(df["close"].rolling(20).std().iloc[-1])
    bb_upper_val = sma20_val + 2 * std20_val
    sma50_val = float(df["close"].rolling(50).mean().iloc[-1]) if len(df) >= 50 else price * 0.92

    if best_strategy == "momentum":
        entry = round(price, 2)
        stop = round(max(price - 2 * atr, sma20_val * 0.97), 2)
        t1 = round(price + 1.5 * (price - stop), 2)
        t2 = round(price + 3.0 * (price - stop), 2)
        note = "Enter on pullback to SMA20; ride the trend"
    elif best_strategy == "swing":
        entry = round(price, 2)
        stop = round(price - 2.0 * atr, 2)
        t1 = round(sma20_val, 2)
        t2 = round(min(bb_upper_val, sma20_val + 2 * abs(sma20_val - stop)), 2)
        note = "Oversold bounce — target BB middle then upper"
    elif best_strategy == "mean_reversion":
        entry = round(price, 2)
        stop = round(price - 1.5 * atr, 2)
        t1 = round(sma20_val, 2)
        t2 = round(bb_upper_val, 2)
        note = "Snap-back to mean (SMA20) then upper BB"
    elif best_strategy == "breakout":
        entry = round(price * 1.005, 2)
        stop = round(price - 1.5 * atr, 2)
        t1 = round(price + 2.0 * (price - stop), 2)
        t2 = round(price + 4.0 * (price - stop), 2)
        note = "Buy the breakout close; stop below breakout level"
    elif best_strategy == "long_term":
        entry = round(price, 2)
        stop = round(max(sma50_val * 0.95, price - 3 * atr), 2)
        t1 = round(price * 1.20, 2)
        t2 = round(price * 1.40, 2)
        note = "Position trade — hold weeks to months"
    else:
        entry = round(price, 2)
        stop = round(price - 2 * atr, 2)
        t1 = round(price + 2 * (price - stop), 2)
        t2 = round(price + 3 * (price - stop), 2)
        note = ""

    stop = max(stop, round(price * 0.80, 2))  # hard floor: max 20% stop
    risk_amt = round(entry - stop, 2)
    risk_pct = round(risk_amt / entry * 100, 1) if entry > 0 else 0
    rr1 = round((t1 - entry) / risk_amt, 1) if risk_amt > 0 else 0
    rr2 = round((t2 - entry) / risk_amt, 1) if risk_amt > 0 else 0

    return {
        "scores": scores,
        "best_strategy": best_strategy,
        "best_score": best_score,
        "rating": stars,
        "verdict": verdict,
        "trade_plan": {
            "entry": entry,
            "stop_loss": stop,
            "target_1": t1,
            "target_2": t2,
            "risk_pct": f"{risk_pct}%",
            "risk_reward_t1": f"1:{rr1}",
            "risk_reward_t2": f"1:{rr2}",
            "note": note,
        },
        "rsi": round(rsi, 1),
        "trend": trend_dir,
        "macd": macd_cross.split("(")[0].strip() if macd_cross else "N/A",
        "bb": "SQUEEZE" if "SQUEEZE" in bb_signal else ("UPPER" if "UPPER" in bb_signal else ("LOWER" if "LOWER" in bb_signal else "MID")),
        "obv": "BULL" if "CONFIRMED UPTREND" in obv_signal or "BULLISH DIV" in obv_signal else ("BEAR" if "CONFIRMED DOWNTREND" in obv_signal or "BEARISH DIV" in obv_signal else "NEUTRAL"),
    }
