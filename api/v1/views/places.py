#!/usr/bin/python3
"""Create a new view for Place objects that handles all default RESTFul API
    actions"""
from models import storage
from models import base_model
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    all_places = []
    for place in city.places:
        all_places.append(place.to_dict())
    return jsonify(all_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def error_place(place_id):
    """ Retrieves a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """create place"""
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)

    json_data = request.get_json()
    if json_data is None:
        abort(400, 'Not a JSON')
    if json_data.get('user_id') is None:
        abort(400, 'Missing user_id')
    user_id = json_data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if json_data.get('name') is None:
        abort(400, 'Missing name')
    json_data['city_id'] = city_id
    place = Place(**json_data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    json_data = request.get_json()
    if json_data is None:
        abort(400, 'Not a JSON')
    for key, value in json_data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
