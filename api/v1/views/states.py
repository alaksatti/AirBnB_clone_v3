#!/usr/bin/python3
''' state file '''
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_state():
    '''return json of all state objects '''
    return jsonify([o.to_dict() for o in storage.all("State").values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    ''' return a state based on its id '''
    state = storage.get('State', state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    ''' delete a state based on its id '''
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    state.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''create a state'''
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400

    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400

    new_state = State(**request.get_json())
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a state object"""
    stored_data = request.get_json()

    if not stored_data:
        return jsonify({'error': 'Not a JSON'}), 400

    retrieved_state = storage.get("State", state_id)
    if retrieved_state is None:
        abort(404)

    for k, v in stored_data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(retrieved_state, k, v)
    storage.save()
    return retrieved_state.to_dict(), 200
