from typing import Optional

import random

# Demo mode always creates visible movement so the system demonstrates active alerts.
DEMO_JITTER_MIN = -0.02
DEMO_JITTER_MAX = 0.02
DEMO_MIN_MOVE = 0.01

# Realistic fallback baselines if yfinance blocks the server IP
MOCK_BASELINES = {
    "AAPL": 175.50,
    "TSLA": 190.20,
    "NVDA": 850.10,
    "MSFT": 410.30,
    "AMZN": 178.90,
    "AMC": 4.50,
    "GME": 15.20,
    "PLTR": 24.10,
}

_current_mock_prices = MOCK_BASELINES.copy()

import requests
from config.settings import FINNHUB_API_KEY

def fetch_price(ticker: str) -> Optional[float]:
    # 1. Try Real Data from Finnhub (works on Render/Cloud)
    if FINNHUB_API_KEY and FINNHUB_API_KEY != "YOUR_FREE_API_KEY_HERE":
        try:
            url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_API_KEY}"
            response = requests.get(url, timeout=5)
            data = response.json()
            if data and 'c' in data and data['c'] > 0:
                price = float(data['c'])
                _current_mock_prices[ticker] = price # Sync mock with real data
                return round(price, 4)
        except Exception as e:
            print(f"Finnhub error for {ticker}: {e}")

    # 2. Fallback to High-Performance Mock Engine (for smooth demo flow)
    price = _current_mock_prices.get(ticker, 100.0)
    
    jitter = random.uniform(DEMO_JITTER_MIN, DEMO_JITTER_MAX)
    if abs(jitter) < DEMO_MIN_MOVE:
        jitter = DEMO_MIN_MOVE if jitter >= 0 else -DEMO_MIN_MOVE

    new_price = float(price) * (1 + jitter)
    _current_mock_prices[ticker] = new_price
    return round(new_price, 4)


def fetch_prices(tickers: list[str]) -> dict[str, Optional[float]]:
    return {ticker: fetch_price(ticker) for ticker in tickers}
