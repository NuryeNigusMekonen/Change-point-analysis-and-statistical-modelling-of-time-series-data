from flask import Flask
from flask_cors import CORS

from routes.prices import prices_bp
from routes.change_points import cp_bp
from routes.events import events_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(prices_bp)
app.register_blueprint(cp_bp)
app.register_blueprint(events_bp)

if __name__ == "__main__":
    app.run(debug=True)
