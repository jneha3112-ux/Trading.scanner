import yfinance as yf
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

def fetch_price(ticker: str) -> Optional[float]:
    # We use the mock engine as the primary source to ensure the demo is INSTANT and robust
    # Cloud IPs (Render/AWS) are often blocked by Yahoo, causing 30s+ timeouts per ticker.
    price = _current_mock_prices.get(ticker, 100.0)
    
    try:
        # We can still try to grab a real price in the background, but we don't let it block
        # For the demo, we'll just stick to the high-performance mock engine
        pass 
    except Exception:
        pass

    jitter = random.uniform(DEMO_JITTER_MIN, DEMO_JITTER_MAX)
    if abs(jitter) < DEMO_MIN_MOVE:
        jitter = DEMO_MIN_MOVE if jitter >= 0 else -DEMO_MIN_MOVE

    new_price = float(price) * (1 + jitter)
    
    # Update the tracking price for the next call
    _current_mock_prices[ticker] = new_price
    
    return round(new_price, 4)


def fetch_prices(tickers: list[str]) -> dict[str, Optional[float]]:
    return {ticker: fetch_price(ticker) for ticker in tickers}
