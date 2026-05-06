import threading
import time
from flask import Flask, jsonify, send_from_directory
from core.scanner import Scanner
from config.settings import POLL_INTERVAL

app = Flask(__name__, static_folder="ui")

scanner = Scanner()
_lock = threading.Lock()


def _run_scanner() -> None:
    scanner.initialize_baselines()
    while True:
        with _lock:
            scanner.scan()
        time.sleep(POLL_INTERVAL)


@app.route("/")
def index():
    return send_from_directory("ui", "index.html")


@app.route("/api/status")
def status():
    with _lock:
        return jsonify(scanner.get_state())


if __name__ == "__main__":
    thread = threading.Thread(target=_run_scanner, daemon=True)
    thread.start()
    print("Dashboard -> http://localhost:5000\n")
    app.run(debug=False, port=5000)
