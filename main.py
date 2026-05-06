import time
import sys
from core.scanner import Scanner
from config.settings import POLL_INTERVAL, ALERT_THRESHOLD


def main() -> None:
    print("=" * 40)
    print("   Real-Time Stock Alert System")
    print("=" * 40)
    print(f"  Threshold : ±{ALERT_THRESHOLD}%")
    print(f"  Interval  : {POLL_INTERVAL}s")
    print("=" * 40 + "\n")

    scanner = Scanner()
    scanner.initialize_baselines()

    print("Monitoring prices. Press Ctrl+C to stop.\n")

    try:
        while True:
            scanner.scan()
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("\nScanner stopped.")
        sys.exit(0)


if __name__ == "__main__":
    main()
