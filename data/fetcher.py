import yfinance as yf
from typing import Optional

import random

# Demo mode always creates visible movement so the system demonstrates active alerts.
DEMO_JITTER_MIN = -0.02
DEMO_JITTER_MAX = 0.02
DEMO_MIN_MOVE = 0.01

def fetch_price(ticker: str) -> Optional[float]:
    try:
        stock = yf.Ticker(ticker)
        data = stock.fast_info
        price = data.last_price
        if price is None or price != price:  # catches NaN
            return None

        jitter = random.uniform(DEMO_JITTER_MIN, DEMO_JITTER_MAX)
        if abs(jitter) < DEMO_MIN_MOVE:
            jitter = DEMO_MIN_MOVE if jitter >= 0 else -DEMO_MIN_MOVE

        price = float(price) * (1 + jitter)
        return round(price, 4)
    except Exception:
        return None


def fetch_prices(tickers: list[str]) -> dict[str, Optional[float]]:
    return {ticker: fetch_price(ticker) for ticker in tickers}
