#!/usr/bin/python3
''' user file '''
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models import storage
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_place(city_id):
    '''return json of all place objects '''
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_by_id(place_id):
    ''' return a place based on its id '''
    place = storage.get('Place', place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    ''' delete a place based on its id '''
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    place.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_places(city_id):
    '''create a place'''
    state = storage.get('City', city_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'user_id' not in request.get_json():
        return jsonify({'error': 'Missing user_id'}), 400

    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400

    user_id = data.get('user_id')
    user = storage.get('User', user_id)
    if not user:
        abort(404)

    new_place = Place(name=data.get('name'), user_id=user_id, city_id=city_id)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates place object"""
    stored_data = request.get_json()

    if not stored_data:
        return jsonify({'error': 'Not a JSON'}), 400

    retrieved_place = storage.get("Place", place_id)
    if retrieved_place is None:
        abort(404)

    for k, v in stored_data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(retrieved_place, k, v)
    storage.save()
    return jsonify(retrieved_place.to_dict()), 200
