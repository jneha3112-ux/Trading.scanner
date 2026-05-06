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
    if FINNHUB_API_KEY and len(FINNHUB_API_KEY) > 10:
        try:
            url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_API_KEY}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data and 'c' in data and data['c'] > 0:
                    price = float(data['c'])
                    _current_mock_prices[ticker] = price # Sync
                    return round(price, 4)
            else:
                print(f"Finnhub API Error: {response.status_code} - {response.text[:50]}")
        except Exception as e:
            print(f"Finnhub request error for {ticker}: {e}")

    # 2. Fallback to High-Performance Mock Engine
    # We use a stable jitter that oscillates around the base price
    base_price = MOCK_BASELINES.get(ticker, 100.0)
    
    # Oscillating jitter (prevents price from flying to infinity)
    # We use the previous price but nudge it back toward the base if it gets too far
    current = _current_mock_prices.get(ticker, base_price)
    drift = (base_price - current) * 0.05 # Pull back to center
    jitter = random.uniform(-0.005, 0.005) # Small natural movement
    
    new_price = current + drift + (current * jitter)
    _current_mock_prices[ticker] = new_price
    
    return round(new_price, 4)


def fetch_prices(tickers: list[str]) -> dict[str, Optional[float]]:
    return {ticker: fetch_price(ticker) for ticker in tickers}
