#!/usr/bin/python3
"""this is flask app"""

from flask_cors import CORS
from flask import Flask
from models import storage
from api.v1.views import app_views
import os
from flask import jsonify

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    error = {"error": "Not found"}
    return jsonify(error), 404


if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
