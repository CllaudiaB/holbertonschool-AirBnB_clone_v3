#!/usr/bin/python3
"""Create a new view for city objects that handles all default RESTFul API
    actions"""
from models import storage
from models import base_model
from api.v1.views import app_views
from models.state import State
from models.city import City
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    all_cities = []
    cities = state.cities()
    for city in cities:
        all_cities.append(city.to_dict())
    return jsonify(all_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def error_city(city_id):
    """ Retrieves a City object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(city_id):
    """create city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    
    json_data = request.get_json()
    if json_data is None:
        abort(400, 'Not a JSON')
    if json_data.get('name') is None:
        abort(400, 'Missing name')
    city = City(**json_data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Updates a City object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    
    json_data = request.get_json()
    if json_data is None:
        abort(400, 'Not a JSON')
    for key, value in json_data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
