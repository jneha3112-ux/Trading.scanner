# Real-Time Stock Alert System

A modular Python + Flask stock alert system with a live web dashboard, sound alerts, and configurable thresholds.

## Quickstart

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the web dashboard (recommended)
python app.py

# 3. Open in browser
http://localhost:5000

# ── OR ── run CLI only
python main.py
```

## Dashboard Features

| Feature               | Description                                         |
|-----------------------|-----------------------------------------------------|
| 📊 Live price cards   | Updates every 5 seconds with flash animation        |
| 📈 Threshold bar      | Visual fill showing how close to alert threshold    |
| 🔔 Alert sound        | 3-note chime via Web Audio API (toggleable)         |
| 🗂 Alert log          | Timestamped history of all triggered alerts         |
| 🟢 Live status badge  | Shows connection + last update time                 |

## Configuration

Edit `config/settings.py`:

| Setting           | Default                                       | Description                     |
|-------------------|-----------------------------------------------|---------------------------------|
| `TICKERS`         | `["AAPL","TSLA","NVDA","MSFT","AMZN"]`        | Stocks to monitor               |
| `POLL_INTERVAL`   | `12`                                          | Seconds between price polls     |
| `ALERT_THRESHOLD` | `5.0`                                         | % move from baseline to alert   |

> **Tip:** Set `ALERT_THRESHOLD = 0.1` for testing — any tiny price tick will trigger alerts.

## Alert Format (CLI)

```
┌────────────────────────────────────┐
│  [ALERT]                           │
│  Ticker : TSLA                     │
│  Change : +5.83%                   │
│  Price  : $245.6700                │
│  Time   : 10:32:15                 │
└────────────────────────────────────┘
```

## Project Structure

```
Trading.scanner/
├── app.py                ← Flask server + background scanner thread
├── main.py               ← CLI-only entry point
├── config/
│   └── settings.py       ← tickers, interval, threshold
├── core/
│   ├── scanner.py        ← baseline tracking, % change, alert log
│   └── alerts.py         ← alert formatting
├── data/
│   └── fetcher.py        ← yfinance price fetching
├── ui/
│   └── index.html        ← web dashboard
├── utils/
│   └── logger.py
└── requirements.txt
```

> **Note:** Yahoo Finance data carries a ~15-minute delay on free feeds. For live demo purposes, lower `ALERT_THRESHOLD` to `0.05`–`0.1` to see alerts fire quickly.
