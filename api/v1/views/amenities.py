#!/usr/bin/python3
''' amenities file '''
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenity():
    '''return json of all amenity objects '''
    return jsonify([o.to_dict() for o in storage.all("Amenity").values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    ''' return a amenity based on its id '''
    amenity = storage.get('Amenity', amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    ''' delete a amenity based on its id '''
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    '''create a state'''
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400

    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400

    new_amenity = Amenity(**request.get_json())
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates amenity object"""
    stored_data = request.get_json()

    if not stored_data:
        return jsonify({'error': 'Not a JSON'}), 400

    retrieved_amenity = storage.get("Amenity", amenity_id)
    if retrieved_amenity is None:
        abort(404)

    for k, v in stored_data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(retrieved_amenity, k, v)
    storage.save()
    return retrieved_amenity.to_dict(), 200
