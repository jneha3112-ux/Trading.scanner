TICKERS = ["TSLA", "NVDA", "PLTR", "AMC", "GME"]
TICKERS = ["AAPL", "TSLA", "NVDA", "MSFT", "AMZN"]

TICKER_NAMES = {
    "AAPL": "Apple",
    "TSLA": "Tesla",
    "NVDA": "NVIDIA",
    "MSFT": "Microsoft",
    "AMZN": "Amazon",
}

POLL_INTERVAL = 12  # seconds

ALERT_THRESHOLD = 5.0  # percentage change to trigger alert

import os

# Get your free API key at https://finnhub.io/register
# Best practice: Add this to Render -> Environment Variables
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "d7tjae9r01qlbd3kd9b0d7tjae9r01qlbd3kd9bg")

