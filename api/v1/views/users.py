#!/usr/bin/python3
''' user file '''
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_user():
    '''return json of all users objects '''
    return jsonify([o.to_dict() for o in storage.all("User").values()])


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_by_id(user_id):
    ''' return a user based on its id '''
    user = storage.get('User', user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    ''' user a user based on its id '''
    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    user.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''create a user'''
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400

    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400

    new_user = User(**request.get_json())
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates user object"""
    stored_data = request.get_json()

    if not stored_data:
        return jsonify({'error': 'Not a JSON'}), 400

    retrieved_user = storage.get("User", user_id)
    if retrieved_user is None:
        abort(404)

    for k, v in stored_data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(retrieved_amenity, k, v)
    storage.save()
    return retrieved_user.to_dict(), 200
