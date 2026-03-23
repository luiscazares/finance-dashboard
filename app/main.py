import os
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from app.data import get_stock, get_crypto

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

app = FastAPI()

app.mount("/static", StaticFiles(directory=os.path.join(ROOT_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(ROOT_DIR, "templates"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://finance.luiscazares.com"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/stock/{ticker}")
async def stock(ticker: str, period: str = "1mo"): 
    return await get_stock(ticker, period)

@app.get("/api/crypto/{coin_id}")
async def crypto(coin_id: str, period: str = "30"):
    return await get_crypto(coin_id, period)