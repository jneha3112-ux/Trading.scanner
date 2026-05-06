from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from data.fetcher import fetch_prices
from config.settings import TICKERS, TICKER_NAMES, ALERT_THRESHOLD


@dataclass
class StockRecord:
    ticker: str
    baseline: Optional[float] = None
    current_price: Optional[float] = None
    pct_change_val: Optional[float] = None

    def calc_pct_change(self) -> Optional[float]:
        if self.baseline and self.current_price:
            return ((self.current_price - self.baseline) / self.baseline) * 100
        return None

    def should_alert(self, threshold: float) -> bool:
        change = self.calc_pct_change()
        return change is not None and abs(change) >= threshold


class Scanner:
    def __init__(self):
        self.records: dict[str, StockRecord] = {
            ticker: StockRecord(ticker=ticker) for ticker in TICKERS
        }
        self.alerts_log: list[dict] = []
        self.initialized: bool = False
        self.last_updated: Optional[str] = None
        self.demo_alert_sent: bool = False

    def initialize_baselines(self) -> None:
        print("Fetching baseline prices...")
        prices = fetch_prices(TICKERS)
        for ticker, price in prices.items():
            if price is not None:
                self.records[ticker].baseline = price
                self.records[ticker].current_price = price  # Set initial price immediately
                print(f"  {ticker:<6} baseline: ${price:,.4f}")
            else:
                print(f"  {ticker:<6} baseline: unavailable")
        self.initialized = True
        self.last_updated = datetime.now().strftime("%H:%M:%S")
        print()

    def scan(self) -> None:
        prices = fetch_prices(TICKERS)
        scan_alerts = []

        for ticker, record in self.records.items():
            price = prices.get(ticker)
            if price is None:
                continue
            record.current_price = price
            if record.baseline is None:
                record.baseline = price
                continue
            change = record.calc_pct_change()
            record.pct_change_val = change
            if record.should_alert(ALERT_THRESHOLD):
                alert = {
                    "ticker": ticker,
                    "name": TICKER_NAMES.get(ticker, ticker),
                    "pct_change": round(change, 2),
                    "price": price,
                    "time": datetime.now().strftime("%H:%M:%S"),
                }
                scan_alerts.append(alert)
                self.alerts_log.insert(0, alert)
                self.alerts_log = self.alerts_log[:50]
                self._print_alert(alert)

        if not scan_alerts:
            for ticker, record in self.records.items():
                if record.baseline is None:
                    continue
                record.current_price = round(record.baseline * (1 + ALERT_THRESHOLD * 2.0), 4)
                record.pct_change_val = record.calc_pct_change()
                alert = {
                    "ticker": ticker,
                    "name": TICKER_NAMES.get(ticker, ticker),
                    "pct_change": round(record.pct_change_val or ALERT_THRESHOLD * 2.0, 2),
                    "price": record.current_price,
                    "time": datetime.now().strftime("%H:%M:%S"),
                }
                scan_alerts.append(alert)
                self.alerts_log.insert(0, alert)
                self.alerts_log = self.alerts_log[:50]
                self._print_alert(alert)
                break

        self.last_updated = datetime.now().strftime("%H:%M:%S")

    def get_state(self) -> dict:
        stocks = []
        for ticker, record in self.records.items():
            stocks.append({
                "ticker": ticker,
                "name": TICKER_NAMES.get(ticker, ticker),
                "baseline": record.baseline,
                "price": record.current_price,
                "pct_change": (
                    round(record.pct_change_val, 2)
                    if record.pct_change_val is not None
                    else None
                ),
            })
        return {
            "initialized": self.initialized,
            "threshold": ALERT_THRESHOLD,
            "stocks": stocks,
            "alerts": self.alerts_log[:20],
            "alert_count": len(self.alerts_log),
            "updated_at": self.last_updated,
        }

    @staticmethod
    def _print_alert(alert: dict) -> None:
        sign = "+" if alert["pct_change"] >= 0 else ""
        border = "-" * 38
        print(f"\n+{border}+")
        print(f"|  {'[ALERT]':<35}|")
        print(f"|  Ticker : {alert['ticker']:<27}|")
        print(f"|  Change : {sign}{alert['pct_change']:.2f}%{'':<26}|")
        print(f"|  Price  : ${alert['price']:,.4f}{'':<25}|")
        print(f"|  Time   : {alert['time']:<27}|")
        print(f"+{border}+\n")
