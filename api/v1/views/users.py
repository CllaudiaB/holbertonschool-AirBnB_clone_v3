#!/usr/bin/python3
"""Create a new view for User object that handles all default RESTFul API
    actions"""
from models import storage
from models import base_model
from api.v1.views import app_views
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    all_users = []
    dict_users = storage.all(User).values()
    for user in dict_users:
        all_users.append(user.to_dict())
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def error_user(user_id):
    """ Retrieves a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a User """
    json_data = request.get_json()
    if json_data is None:
        abort(400, 'Not a JSON')
    if json_data.get('email') is None:
        abort(400, 'Missing email')
    if json_data.get('password') is None:
        abort(400, 'Missing password')
    user = User(**json_data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Updates a User object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        abort(400, 'Not a JSON')
    for key, value in json_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
