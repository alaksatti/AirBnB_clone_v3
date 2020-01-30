#!/usr/bin/python3
''' place_amenity file '''
from api.v1.views import app_views
from models.amenity import Amenity
from models.place import Place
from models import storage
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenity(place_id):
    '''return json of all amenity objects '''
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    amenity = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenity)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    ''' delete amenity based on its id '''
    place = storage.get('Place', place_id)
    if place:
        amenity = storage.get('Amenity', amenity_id)
        if amenity:
            if amenity in place.amenities:
                place.amenities.remove(amenity)
                storage.save()
                return jsonify({}), 200
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def create_place_amenity(place_id, amenity_id):
    '''create a place_amenity'''
    place = storage.get('Place', place_id)
    if place:
        amenity = storage.get('Amenity', amenity_id)
        if amenity:
            if amenity in place.amenities:
                return jsonify(amenity.to_dict()), 200
            else:
                place.amenities.append(amenity)
                storage.save()
                return jsonify(amenity.to_dict()), 201
    abort(404)
