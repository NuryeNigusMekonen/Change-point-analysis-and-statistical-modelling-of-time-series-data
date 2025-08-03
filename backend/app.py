from flask import Flask, jsonify, send_from_directory

import json

app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")

@app.route("/api/data")
def get_data():
    # Example: Load precomputed change point results
    with open("../data/global_events.json", "r") as f:
        result = json.load(f)

    return jsonify(result)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    from os import path as osp
    if path != "" and osp.exists(osp.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")
