import yfinance as yf
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
COINGECKO_URL = os.getenv("COINGECKO_API_URL")

async def get_stock(ticker: str):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")
    return {
        "ticker": ticker,
        "current_price": round(hist["Close"].iloc[-1], 2),
        "history": [
            {"date": str(d.date()), "close": round(v, 2)}
            for d, v in hist["Close"].items()
        ]
    }

async def get_crypto(coin_id: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{COINGECKO_URL}/coins/{coin_id}/market_chart",
            params={"vs_currency": "usd", "days": "30"}
        )
        data = r.json()
    prices = data.get("prices", [])
    return {
        "coin": coin_id,
        "current_price": round(prices[-1][1], 2) if prices else None,
        "history": [
            {"date": str(int(p[0] / 1000)), "close": round(p[1], 2)}
            for p in prices
        ]
    }