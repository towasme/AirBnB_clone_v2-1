#!/usr/bin/python3
""" script that instance a flask variable """
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, make_response
from os import getenv

host = getenv('0.0.0.0')
port = getenv('5000')
app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.errorhandler(404)
def error_404(self):
    """ Error: 404 Not Found,create a handler for 404
        errors that returns a JSON-formatted 404
        status code response.
    """
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def teardown_db(self):
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
