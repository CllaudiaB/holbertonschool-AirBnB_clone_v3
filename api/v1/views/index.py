#!/usr/bin/python3
""" create a file index.py """


from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage



@app_views.route('/status')
def status():
    """ returns a JSON: "status": "OK" """
    return jsonify({'status': 'OK'})

@app_views.route('/stats')
def stats():
    """retrieves the number of each objects by type"""
    return  jsonify({"amenities": storage.count(Amenity),
                    "cities": storage.count(City),
                    "places": storage.count(Place),
                    "reviews": storage.count(Review),
                    "states": storage.count(State),
                    "users": storage.count(User)
                     })
