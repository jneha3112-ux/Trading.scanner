from datetime import datetime


def trigger_alert(ticker: str, pct_change: float, price: float) -> None:
    sign = "+" if pct_change >= 0 else ""
    timestamp = datetime.now().strftime("%H:%M:%S")

    border = "─" * 36
    print(f"\n┌{border}┐")
    print(f"│  {'[ALERT]':<33}│")
    print(f"│  Ticker : {ticker:<25}│")
    print(f"│  Change : {sign}{pct_change:.2f}%{'':<24}│")
    print(f"│  Price  : ${price:,.4f}{'':<24}│")
    print(f"│  Time   : {timestamp:<25}│")
    print(f"└{border}┘\n")
