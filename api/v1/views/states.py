#!/usr/bin/python3
"""Create a new view for State objects that handles all default RESTFul API actions"""

from models import storage
from models import base_model
from api.v1.views import app_views
from models.state import State
from flask import jsonify, abort

@app_views.route('/states', methods=['GET'])
def states():
    """Retrieves the list of all State objects"""
    all_states = [] 
    dict_states = storage.all(State).values()
    for state in dict_states:
        all_states.append(state.to_dict())
    return jsonify(all_states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def error_state(state_id):
    """ Retrieves a State object """
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200