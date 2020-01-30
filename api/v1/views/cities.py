#!/usr/bin/python3
''' city file '''
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_city(state_id):
    '''return json of all city objects '''
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    cities = []

    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    ''' return a city based on its id '''
    city = storage.get('City', city_id)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    ''' delete a city based on its id '''
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    city.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    '''create a city'''
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    stored_data = request.get_json()
    if not stored_data:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400

    new_city = City(name=stored_data.get('name'), state_id=state_id)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a city object"""
    stored_data = request.get_json()
    if not stored_data:
        return jsonify({'error': 'Not a JSON'}), 400

    retrieved_city = storage.get("City", city_id)
    if retrieved_city is None:
        abort(404)

    for k, v in stored_data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(retrieved_city, k, v)
    storage.save()
    return retrieved_city.to_dict(), 200
