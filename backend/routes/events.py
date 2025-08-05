from flask import Blueprint, jsonify, request
import pandas as pd
import os

events_bp = Blueprint("events", __name__)
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))

@events_bp.route("/api/events", methods=["GET"])
def get_events():
    try:
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        file_path = os.path.join(DATA_DIR, "key_events.csv")
        df = pd.read_csv(file_path)

        # Rename columns lowercase for consistency if needed
        df.columns = [col.lower() for col in df.columns]

        # The event CSV has columns: event, start_date, region, type, notes
        df["start_date"] = pd.to_datetime(df["start_date"], format="%Y-%m-%d", errors="coerce")

        df = df.dropna(subset=["start_date", "event"])

        if start_date:
            df = df[df["start_date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["start_date"] <= pd.to_datetime(end_date)]

        df = df.sort_values("start_date")
        df["start_date"] = df["start_date"].dt.strftime("%Y-%m-%d")

        # Return only event and date (as start_date)
        result = df[["start_date", "event", "notes"]].rename(columns={"start_date": "date"})


        return jsonify(result.to_dict(orient="records"))

    except Exception as e:
        print("Error in /api/events:", e)
        return jsonify({"error": str(e)}), 500
