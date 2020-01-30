#!/usr/bin/python3
''' user file '''
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models import storage
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    '''return json of all reviews objects '''
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_by_id(review_id):
    ''' return a review based on its id '''
    review = storage.get('Review', review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    ''' delete a review based on its id '''
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)

    review.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    '''create a place'''
    place = storage.get('Place', place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'user_id' not in request.get_json():
        return jsonify({'error': 'Missing user_id'}), 400

    if 'text' not in request.get_json():
        return jsonify({'error': 'Missing text'}), 400

    user_id = data.get('user_id')
    user = storage.get('User', user_id)
    if not user:
        abort(404)

    new_review = Review(name=data.get('name'), user_id=user_id, place_id=place_id)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates review object"""
    stored_data = request.get_json()

    if not stored_data:
        return jsonify({'error': 'Not a JSON'}), 400

    retrieved_review = storage.get("Review", review_id)
    if retrieved_review is None:
        abort(404)

    for k, v in stored_data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(retrieved_review, k, v)
    storage.save()
    return jsonify(retrieved_review.to_dict()), 200
