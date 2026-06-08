"""DSE data layer — wraps bdshare with correct API signatures."""
from datetime import datetime, timedelta

import pandas as pd


def _safe_float(val):
    try:
        return float(str(val).replace(",", "").replace("%", "").strip())
    except (ValueError, TypeError):
        return None


def get_live_price(symbol: str) -> dict:
    import bdshare
    symbol = symbol.upper().strip()
    try:
        df = bdshare.get_current_trade_data(symbol=symbol)
        if df is None or df.empty:
            return {"error": f"No data for {symbol}"}
        row = df.iloc[0]
        return {
            "symbol": symbol,
            "last_price": _safe_float(row.get("ltp")),
            "open": _safe_float(row.get("open")),
            "high": _safe_float(row.get("high")),
            "low": _safe_float(row.get("low")),
            "close": _safe_float(row.get("close")),
            "yesterday_close": _safe_float(row.get("ycp")),
            "change": _safe_float(row.get("change")),
            "volume": _safe_float(row.get("volume")),
            "trade_count": _safe_float(row.get("trade")),
            "value_mn": _safe_float(row.get("value")),
        }
    except Exception as e:
        return {"error": str(e), "symbol": symbol}


def get_historical_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    import bdshare
    symbol = symbol.upper().strip()
    try:
        df = bdshare.get_hist_data(start=start_date, end=end_date, code=symbol)
    except Exception:
        try:
            df = bdshare.get_historical_data(start=start_date, end=end_date, code=symbol)
        except Exception as e:
            return pd.DataFrame()

    if df is None or df.empty:
        return pd.DataFrame()

    # Normalize column names
    df.columns = [c.lower().strip() for c in df.columns]

    # Use 'close' as the canonical close price (more accurate than ltp)
    # Remove 'ltp' to avoid duplicates after rename
    if "close" in df.columns and "ltp" in df.columns:
        df = df.drop(columns=["ltp"])

    rename_map = {}
    for col in df.columns:
        if col == "open":
            rename_map[col] = "open"
        elif col == "high":
            rename_map[col] = "high"
        elif col == "low":
            rename_map[col] = "low"
        elif col in ("close", "closep", "ltp"):
            rename_map[col] = "close"
        elif col == "volume":
            rename_map[col] = "volume"
    df = df.rename(columns=rename_map)

    for col in ["open", "high", "low", "close", "volume"]:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(",", ""), errors="coerce"
            )

    # Ensure datetime index
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date")
    elif not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)

    df = df.sort_index()

    # Drop rows where close is NaN
    if "close" in df.columns:
        df = df.dropna(subset=["close"])

    return df


def get_all_live_prices() -> list[dict]:
    import bdshare
    try:
        df = bdshare.get_current_trade_data()
        if df is None or df.empty:
            return []
        results = []
        for _, row in df.iterrows():
            results.append({
                "symbol": str(row.get("symbol", "")).strip(),
                "last_price": _safe_float(row.get("ltp") or row.get("close")),
                "change": _safe_float(row.get("change")),
                "volume": _safe_float(row.get("volume")),
                "value_mn": _safe_float(row.get("value")),
            })
        return results
    except Exception as e:
        return [{"error": str(e)}]


def get_market_summary() -> dict:
    import bdshare
    try:
        df = bdshare.get_market_info()
        if df is None or df.empty:
            return {"error": "No market data"}
        # Most recent row
        row = df.iloc[0]
        return {
            "date": str(row.get("Date", "")),
            "DSEX": _safe_float(row.get("DSEX Index")),
            "DSES": _safe_float(row.get("DSES Index")),
            "DS30": _safe_float(row.get("DS30 Index")),
            "total_trades": int(row.get("Total Trade", 0) or 0),
            "total_volume": int(row.get("Total Volume", 0) or 0),
            "total_value_mn": _safe_float(row.get("Total Value (mn)")),
            "market_cap_mn": _safe_float(row.get("Total Market Cap. (mn)")),
            "recent_sessions": df.head(5).to_dict(orient="records"),
        }
    except Exception as e:
        return {"error": str(e)}


def get_top_gainers(n: int = 10) -> list[dict]:
    stocks = get_all_live_prices()
    if not stocks or (len(stocks) == 1 and "error" in stocks[0]):
        return stocks
    valid = [s for s in stocks if s.get("change") is not None]
    return sorted(valid, key=lambda x: x["change"], reverse=True)[:n]


def get_top_losers(n: int = 10) -> list[dict]:
    stocks = get_all_live_prices()
    if not stocks or (len(stocks) == 1 and "error" in stocks[0]):
        return stocks
    valid = [s for s in stocks if s.get("change") is not None]
    return sorted(valid, key=lambda x: x["change"])[:n]


def get_company_info(symbol: str) -> dict:
    import bdshare
    symbol = symbol.upper().strip()
    try:
        # get_latest_pe returns unlabelled columns: [symbol, ltp, ycp, pe, ?, ?, ?, eps, nav]
        df = bdshare.get_latest_pe()
        if df is None or df.empty:
            return {"error": "No PE data available", "symbol": symbol}

        # Find the row matching the symbol (column 0)
        match = df[df.iloc[:, 0].astype(str).str.strip().str.upper() == symbol]
        if match.empty:
            return {"error": f"No fundamental data found for {symbol}", "symbol": symbol}

        row = match.iloc[0]
        return {
            "symbol": symbol,
            "last_price": _safe_float(row.iloc[1]) if len(row) > 1 else None,
            "yesterday_close": _safe_float(row.iloc[2]) if len(row) > 2 else None,
            "pe_ratio": _safe_float(row.iloc[3]) if len(row) > 3 else None,
            "eps": _safe_float(row.iloc[7]) if len(row) > 7 else None,
            "nav": _safe_float(row.iloc[8]) if len(row) > 8 else None,
        }
    except Exception as e:
        return {"error": str(e), "symbol": symbol}


def get_historical_data_with_live(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Historical OHLCV merged with today's live candle (if market is open)."""
    df = get_historical_data(symbol, start_date, end_date)

    try:
        live = get_live_price(symbol)
        if "error" in live or live.get("last_price") is None:
            return df

        today = pd.Timestamp(datetime.today().date())

        # Skip if today's session is already in the archive
        if not df.empty and today in df.index:
            return df

        row = {
            "open":   live.get("open")   or live.get("last_price"),
            "high":   live.get("high")   or live.get("last_price"),
            "low":    live.get("low")    or live.get("last_price"),
            "close":  live.get("last_price"),
            "volume": live.get("volume") or 0,
        }
        today_df = pd.DataFrame([row], index=[today])
        df = pd.concat([df, today_df]).sort_index()
    except Exception:
        pass  # live fetch failed — return archive data as-is

    return df


def default_date_range(days: int = 365) -> tuple[str, str]:
    end = datetime.today()
    start = end - timedelta(days=days)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")
