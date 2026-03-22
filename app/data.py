import os
from datetime import datetime

import httpx
import yfinance as yf
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()
COINGECKO_URL = os.getenv("COINGECKO_API_URL", "https://api.coingecko.com/api/v3")


def _to_date(ts_ms: float) -> str:
    """Convert millisecond timestamp to YYYY-MM-DD format."""
    return datetime.fromtimestamp(ts_ms / 1000).strftime("%Y-%m-%d")


async def get_stock(ticker: str, period: str = "1mo"):
    """Fetch stock data from Yahoo Finance."""
    ticker = (ticker or "").strip().upper()
    if not ticker:
        raise HTTPException(status_code=400, detail="Ticker is required.")

    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to fetch stock data.",
        ) from exc

    if hist.empty or "Close" not in hist.columns:
        raise HTTPException(
            status_code=404,
            detail=f"Stock '{ticker}' not found.",
        )

    close_series = hist["Close"]
    return {
        "ticker": ticker,
        "period": period,
        "current_price": round(float(close_series.iloc[-1]), 2),
        "history": [
            {"date": str(index.date()), "close": round(float(value), 2)}
            for index, value in close_series.items()
        ],
    }


async def get_crypto(coin_id: str, period: str = "30"):
    """Fetch cryptocurrency data from CoinGecko."""
    coin_id = (coin_id or "").strip().lower()
    if not coin_id:
        raise HTTPException(status_code=400, detail="coin_id is required.")

    if not COINGECKO_URL:
        raise HTTPException(status_code=500, detail="COINGECKO_API_URL is not set.")

    url = f"{COINGECKO_URL.rstrip('/')}/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": period}

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            payload = resp.json()
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise HTTPException(
                status_code=404, detail=f"Coin '{coin_id}' not found."
            ) from exc
        raise HTTPException(status_code=502, detail="CoinGecko API error.") from exc
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail="Network error contacting CoinGecko.",
        ) from exc
    except ValueError:
        raise HTTPException(status_code=502, detail="Invalid response from CoinGecko.")

    prices = payload.get("prices", [])
    if not prices:
        raise HTTPException(
            status_code=404,
            detail=f"No crypto history returned for '{coin_id}'.",
        )

    history = []
    for point in prices:
        if not isinstance(point, (list, tuple)) or len(point) < 2:
            continue
        ts_ms, close = point[0], point[1]
        try:
            history.append(
                {"date": _to_date(ts_ms), "close": round(float(close), 2)}
            )
        except Exception:
            continue

    if not history:
        raise HTTPException(
            status_code=404, detail="No valid crypto history data found."
        )

    return {
        "coin": coin_id,
        "period": period,
        "current_price": round(float(history[-1]["close"]), 2),
        "history": history,
    }