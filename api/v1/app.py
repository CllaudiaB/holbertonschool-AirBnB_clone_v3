#!/usr/bin/python3
""" create file app """
from os import getenv
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

@app.teardown_appcontext
def teardown():
    """ closes the storage on teardown """
    storage.close()

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    
    app.run(host = '0.0.0.0', port = '5000', threaded=True)
