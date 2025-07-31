from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
EVENT_FILE = DATA_DIR / "key_events.csv"
PRICE_FILE = DATA_DIR / "brent_prices.csv"
