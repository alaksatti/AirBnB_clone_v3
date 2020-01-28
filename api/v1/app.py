#!/usr/bin/python3
'''status endpoint for API '''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import models
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    ''' teardown db '''
    models.storage.close()


if __name__ == '__main__':
    host = HBNB_API_HOST or 0.0.0.0
    port = HBNB_API_PORT or 5000

    app.run(host=host, port=port, threaded=True, debug=True)
