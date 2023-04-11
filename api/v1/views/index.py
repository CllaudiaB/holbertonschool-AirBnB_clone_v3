#!/usr/bin/python3
""" create a file index.py """


from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def views_json():
    """ returns a JSON: "status": "OK" """
    return jsonify({'status': 'OK'})
