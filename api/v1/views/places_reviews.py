#!/usr/bin/python3
"""Create a new view for city objects that handles all default RESTFul API
    actions"""
from models import storage
from models import base_model
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User

from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review(place_id):
    """Retrieves the list of all Review objects of a State"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    all_review = []
    for review in place.reviews:
        all_review.append(review.to_dict())
    return jsonify(all_review)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def error_review(review_id):
    """ Retrieves a Review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """create a Review """
    place = storage.get(Place, place_id)
    if place is None:
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
    if json_data.get('text') is None:
        abort(400, 'Missing text')

    json_data['place_id'] = place_id
    review = Review(**json_data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Updates a Review  object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    json_data = request.get_json()
    if json_data is None:
        abort(400, 'Not a JSON')
    for key, value in json_data.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
