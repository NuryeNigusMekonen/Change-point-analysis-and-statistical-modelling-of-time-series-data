from flask import Blueprint, jsonify, request
import pandas as pd
import os

prices_bp = Blueprint("prices", __name__)
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))

@prices_bp.route("/api/prices", methods=["GET"])
def get_prices():
    try:
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        file_path = os.path.join(DATA_DIR, "brent_prices.csv")
        df = pd.read_csv(file_path)

        # Rename columns to lowercase for consistency if needed
        df.columns = [col.lower() for col in df.columns]

        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df = df.dropna(subset=["date", "price"])

        if start_date:
            df = df[df["date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["date"] <= pd.to_datetime(end_date)]

        df = df.sort_values("date")
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")

        return jsonify(df[["date", "price"]].to_dict(orient="records"))

    except Exception as e:
        print("Error in /api/prices:", e)
        return jsonify({"error": str(e)}), 500
