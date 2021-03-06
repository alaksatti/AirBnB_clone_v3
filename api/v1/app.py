#!/usr/bin/python3
'''status endpoint for API '''
from flask import Flask, jsonify
from flask_cors import CORS
import models
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
CORS = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def eror_404_error(self):
    ''' 404 error json format'''
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown(self):
    ''' tear down db '''
    models.storage.close()


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST') or '0.0.0.0'
    port = getenv('HBNB_API_PORT') or '5000'

    app.run(host=host, port=port, threaded=True, debug=True)
