import yfinance as yf
import httpx
import os
from dotenv import load_dotenv
from datetime import datetime
from fastapi import HTTPException

load_dotenv()
COINGECKO_URL = os.getenv("COINGECKO_API_URL")

# app/data.py

async def get_stock(ticker: str, period: str = "1mo"):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period) 

    if hist.empty:
        raise HTTPException(
            status_code=404, 
            detail=f"No data found for ticker '{ticker}' with period '{period}'."
        )

    return {
        "ticker": ticker,
        "current_price": round(hist["Close"].iloc[-1], 2),
        "history": [
            {"date": str(d.date()), "close": round(v, 2)}
            for d, v in hist["Close"].items()
        ]
    }

async def get_crypto(coin_id: str, period: str = "30"):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{COINGECKO_URL}/coins/{coin_id}/market_chart",
            params={"vs_currency": "usd", "days": period}
        )
        
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail="Coin not found or API error")
            
        data = r.json()
    
    prices = data.get("prices", [])
    
    return {
        "coin": coin_id,
        "current_price": round(prices[-1][1], 2) if prices else None,
        "history": [
            {
                # 3. Convert timestamp to YYYY-MM-DD to fix "Invalid Date"
                "date": datetime.fromtimestamp(p[0] / 1000).strftime("%Y-%m-%d"), 
                "close": round(p[1], 2)
            }
            for p in prices
        ]
    }