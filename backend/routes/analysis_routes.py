from flask import Blueprint, jsonify, request
from utils.load_data import load_prices, load_events, load_trace

router = Blueprint("analysis", __name__)

@router.route("/api/prices")
def prices():
    df = load_prices()
    return jsonify(df.to_dict(orient="records"))

@router.route("/api/events")
def events():
    df = load_events()
    return jsonify(df.to_dict(orient="records"))

@router.route("/api/change-points/<cp_type>")
def change_points(cp_type):
    try:
        trace = load_trace(cp_type)
        cps = {}
        if "tau_pos" in trace:
            cps = {"cp": trace["tau_pos"].values.tolist()}
        elif "cp" in trace:
            cps = {"cp": trace["cp"].values.tolist()}
        return jsonify(cps)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
