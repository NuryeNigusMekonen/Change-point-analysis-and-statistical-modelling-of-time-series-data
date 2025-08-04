import pandas as pd
import xarray as xr
import os

def load_prices():
    return pd.read_csv("../data/brent_prices.csv", parse_dates=["date"])

def load_events():
    return pd.read_csv("../data/key_events.csv", parse_dates=["date"])

def load_trace(trace_type):
    trace_path = f"models/trace_{trace_type}.nc"
    if not os.path.exists(trace_path):
        raise FileNotFoundError(f"{trace_path} not found.")
    return xr.load_dataset(trace_path)
