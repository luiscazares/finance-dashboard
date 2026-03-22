# Finance Dashboard

A modern, real-time financial data dashboard built with FastAPI that tracks stock prices and cryptocurrency values with historical data visualization.

## Project Description

Finance Dashboard is a web application that provides:
- **Real-time stock price tracking** via Yahoo Finance (yfinance)
- **Cryptocurrency monitoring** via CoinGecko API
- **Historical price charts** for both stocks and digital assets
- **Responsive web interface** with dynamic chart visualization

The backend is powered by FastAPI with async support, while the frontend uses vanilla JavaScript with Chart.js for visualizations.

## Tech Stack

- **Backend**: FastAPI, Uvicorn
- **Data Sources**: yfinance, CoinGecko API
- **Frontend**: Jinja2 Templates, HTML/CSS/JavaScript, Chart.js
- **HTTP Client**: httpx
- **Environment**: python-dotenv

## Setup Steps

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd finance-dashboard
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root directory with the following configuration:

```env
# CoinGecko API Configuration (Required for crypto endpoints)
COINGECKO_API_URL=https://api.coingecko.com/api/v3
```

**Note**: The `COINGECKO_API_URL` defaults to the public CoinGecko endpoint if not set. If you have a custom API endpoint or API key, specify it here.

## Run Instructions

### Development Server

Start the development server with auto-reload enabled:

```bash
uvicorn app.main:app --reload
```

The application will be available at `http://localhost:8000`

### Production Server

Start the production server with recommended settings:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Interactive API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Dashboard

- **GET** `/` - Main dashboard page with interactive charts

### Stock Data

- **GET** `/api/stock/{ticker}?period={period}` - Get stock price data
  - `ticker` (required): Stock ticker symbol (e.g., "AAPL", "GOOGL", "TSLA")
  - `period` (optional, default: "1mo"): Time period for historical data
    - Valid values: "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"

### Cryptocurrency Data

- **GET** `/api/crypto/{coin_id}?period={days}` - Get cryptocurrency price data
  - `coin_id` (required): CoinGecko coin ID (e.g., "bitcoin", "ethereum", "cardano")
  - `period` (optional, default: "30"): Number of days of historical data (1-365 or "max")

## Usage Examples

### Stock Endpoints

#### Get Apple Stock Data
```bash
curl "http://localhost:8000/api/stock/AAPL"
```

#### Get Tesla Stock Data (3 Months)
```bash
curl "http://localhost:8000/api/stock/TSLA?period=3mo"
```

#### Get Microsoft Stock Data (1 Year)
```bash
curl "http://localhost:8000/api/stock/MSFT?period=1y"
```

### Cryptocurrency Endpoints

#### Get Bitcoin Price (Last 30 Days)
```bash
curl "http://localhost:8000/api/crypto/bitcoin"
```

#### Get Ethereum Price (Last 90 Days)
```bash
curl "http://localhost:8000/api/crypto/ethereum?period=90"
```

#### Get Cardano Price (Last 7 Days)
```bash
curl "http://localhost:8000/api/crypto/cardano?period=7"
```

### Example Response (Stock)

```json
{
  "ticker": "AAPL",
  "period": "1mo",
  "current_price": 175.42,
  "history": [
    {"date": "2026-02-20", "close": 172.15},
    {"date": "2026-02-21", "close": 173.88},
    {"date": "2026-02-22", "close": 175.42}
  ]
}
```

### Example Response (Crypto)

```json
{
  "coin": "bitcoin",
  "period": "30",
  "current_price": 45250.75,
  "history": [
    {"date": "2026-02-20", "close": 42100.50},
    {"date": "2026-02-21", "close": 43500.25},
    {"date": "2026-02-22", "close": 45250.75}
  ]
}
```

## Popular Stock Tickers

**Technology**: AAPL, GOOGL, MSFT, TSLA, META, NVDA, AMD, INTC  
**Finance**: JPM, GS, BAC, WFC, MS  
**Healthcare**: JNJ, PFE, AbbV, MRK, LLY  
**Energy**: XOM, CVX, COP, MPC

## Popular Cryptocurrencies

bitcoin, ethereum, cardano, solana, polkadot, ripple (xrp), litecoin, dogecoin, chainlink, uniswap

## Error Handling

### Stock Endpoint Errors

- **400 Bad Request**: Empty or invalid ticker
  ```json
  {"detail": "Ticker is required."}
  ```

- **404 Not Found**: Invalid ticker or no data available
  ```json
  {"detail": "No data found for ticker 'INVALID'."}
  ```

- **502 Bad Gateway**: Unable to fetch stock data
  ```json
  {"detail": "Unable to fetch stock data."}
  ```

### Crypto Endpoint Errors

- **400 Bad Request**: Empty or invalid coin ID
  ```json
  {"detail": "coin_id is required."}
  ```

- **404 Not Found**: Coin not found or no price history
  ```json
  {"detail": "Coin 'invalid' not found."}
  ```

- **502 Bad Gateway**: Network or API error
  ```json
  {"detail": "Unable to contact CoinGecko."}
  ```

## CORS Configuration

For production, update the CORS allowed origins in `app/main.py`:

```python
allow_origins=["https://yourdomain.com"]
```

Replace with your actual production domain.

## Project Structure

```
finance-dashboard/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and routes
│   ├── data.py          # Stock and crypto data fetching
│   ├── database.py      # Database configuration
│   └── models.py        # Data models (ORM)
├── static/
│   ├── css/
│   │   └── styles.css   # Dashboard styling
│   └── js/
│       └── dashboard.js # Frontend logic
├── templates/
│   └── index.html       # Main dashboard template
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (git-ignored)
└── README.md           # This file
```

## Development Notes

### Adding New Endpoints

1. Add route handler in `app/main.py`
2. Implement logic in `app/data.py`
3. Update frontend templates as needed

### Testing

Visit http://localhost:8000/docs for interactive Swagger UI to test all endpoints.

## Deployment

For production deployment:

1. Set `allow_origins` in `app/main.py` to your domain
2. Use a production ASGI server: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app`
3. Ensure `.env` is configured with your production API URLs
4. Use environment variables for sensitive data

## License

[Add your license here]

## Support

For issues or questions, please create an issue in the repository.
