#!/usr/bin/python3
''' Route for State objects'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage
 
@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    '''route for states'''
    if request.method == 'GET':
       get_states = storage.all('State')
       get_states = list(obj.to_json() for obj in get_states.values())
       return jsonify(get_states)
    if request.method == 'POST':
        data = request.get_json()
        if data is None or type(data) != dict:
            return jsonify({'error' : 'Noy a JSON'}), 400
        name = data.get('name')
        if name is None:
            return jsonify({'error' : 'Missing name'}), 400
        new_obj = State(**data)
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201




@app_views.route('/states/<string:state_id>', methods=['GET', 'PUT', 'DELETE'])
def states_id(state_id=None):
    '''route for states by specififc id'''
    obj = storage.get('State', state_id)
    if obj is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(obj.to_jason())

    if request.method == 'DELETE':
        state_obj.delete()
        del state_obj
        return jsonify({})

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        state_obj.update(req_json)
        return jsonify(state_obj.to_json())
