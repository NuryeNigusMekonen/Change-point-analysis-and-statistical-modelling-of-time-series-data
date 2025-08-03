import pandas as pd
import json
from config import Config
import os

def load_dashboard_data():
    prices_path = os.path.join(Config.DATA_FOLDER, "brent_prices.csv")
    change_points_path = os.path.join(Config.DATA_FOLDER, "change_points.csv")
    events_path = os.path.join(Config.DATA_FOLDER, "global_events.json")

    prices_df = pd.read_csv(prices_path)
    change_df = pd.read_csv(change_points_path)

    with open(events_path, "r") as f:
        events = json.load(f)

    return {
        "prices": prices_df.to_dict(orient="records"),
        "change_points": change_df.to_dict(orient="records"),
        "events": events
    }
