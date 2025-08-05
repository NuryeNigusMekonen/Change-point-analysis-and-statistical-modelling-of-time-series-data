from flask import Blueprint, jsonify
import arviz as az
import os
import numpy as np
import pandas as pd

cp_bp = Blueprint("change_points", __name__)
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../../models")
DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data")

@cp_bp.route("/api/change_points/<string:type>", methods=["GET"])
def get_change_points(type):
    file_map = {
        "mean": "trace_mean.nc",
        "trend": "trace_trend.nc",
        "var": "trace_var.nc"
    }

    filename = file_map.get(type)
    if not filename:
        return jsonify({"error": "Invalid change point type"}), 400

    # Load full price data (to map indices to dates)
    prices_path = os.path.join(DATA_DIR, "brent_prices.csv")
    df_prices = pd.read_csv(prices_path)
    df_prices.columns = [c.lower() for c in df_prices.columns]
    df_prices["date"] = pd.to_datetime(df_prices["date"], format="%d-%b-%y", errors="coerce")

    df_prices = df_prices.dropna(subset=["date"])
    df_prices = df_prices.sort_values("date").reset_index(drop=True)

    path = os.path.join(MODEL_DIR, filename)
    trace = az.from_netcdf(path)

    if type == "mean":
        idxs = trace.posterior["tau_pos"].values.flatten()
    else:
        idxs = trace.posterior["cp"].values.flatten()

    unique_idxs = np.unique(idxs).astype(int)

    # Map indices to actual dates (as strings)
    dates = []
    for idx in unique_idxs:
        if 0 <= idx < len(df_prices):
            dates.append(df_prices.iloc[idx]["date"].strftime("%Y-%m-%d"))

    return jsonify({"change_points": dates})
