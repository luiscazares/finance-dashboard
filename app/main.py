from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from app.data import get_stock, get_crypto

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, change to ["https://finance.luiscazares.com"]
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