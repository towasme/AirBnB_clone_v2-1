#!/usr/bin/python3
""" script that instance a flask variable """

from api.v1.views import app_views
from models import storage
from flask import Flask


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/api/v1/<text>')
def error():
    """ return a json status error """
    answer = {"error": "Not found"}
    return jsonify(answer)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
