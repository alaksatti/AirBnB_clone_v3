#!/usr/bin/python3
''' index'''
from api.v1.views import app_views
from flask import jsonify, request
from models import storage

@app_views.route('/status')
def status():
    ''' status of API route '''
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def stats():
    ''' retrieves the number of each object by type'''
    if request.method == 'GET':
        output = {}
        classes = {
            "Amenitiy" : "amenities",
            "City" : "cities",
            "Place" : "places",
            "Review" : "reviews",
            "State" : "states",
            "User": "users"
        }
    for key, value in classes.items():
        output[value] = storage.count(key)
    return jsonify(output)
