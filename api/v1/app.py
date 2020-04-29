#!/usr/bin/python3
""" script that instance a flask variable """

from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, make_response, abort
import os


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.errorhandler(404)
def error_404(exception):
    """ Error: 404 Not Found,create a handler for 404
        errors that returns a JSON-formatted 404
        status code response. 
    """
    code_except = exception.__str__().split()[0]
    description = exception.description
    return make_response(jsonify({"error": "Not found"}), code_except)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
