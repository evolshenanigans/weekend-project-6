import json
from urllib import response
from flask import Blueprint, request, jsonify
from initiald_inventory.helpers import token_required
from initiald_inventory.models import db, User,Initiald, initiald_schema, initialds_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return {'some': 'value'}

#create car endpoint

@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    name = request.json['name']
    description = request.json['description']
    model = request.json['model']
    year = request.json['year']
    engine = request.json['engine']
    max_speed = request.json['max_speed']
    owner = request.json['owner']
    weight = request.json['weight']
    spec_version = request.json['spec_version']
    series = request.json['series']
    user_token = current_user_token.token

    print(f"BIG TESTER: {current_user_token}")

    initiald = Initiald(name, description, model, year, engine, max_speed, owner, weight, spec_version, series, user_token = user_token )

    db.session.add(initiald)
    db.session.commit()

    response = initiald_schema.dump(initiald)
    return jsonify(response)

#retreive all endpoints
@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Initiald.query.filter_by(user_token = owner).all()
    response = initialds_schema.dump(cars)
    return jsonify(response)

#retreive one car
@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        cars = Initiald.query.get(id)
        response = initiald_schema.dump(cars)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401

#update drone endpoint
@api.route('/cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    cars = Initiald.query.get(id)

    cars.name = request.json['name']
    cars.description = request.json['description']
    cars.model = request.json['model']
    cars.year = request.json['year']
    cars.engine = request.json['engine']
    cars.max_speed = request.json['max_speed']
    cars.owner = request.json['owner']
    cars.weight = request.json['weight']
    cars.spec_version = request.json['spec_version']
    cars.series = request.json['series']
    cars.user_token = current_user_token.token

    db.session.commit()
    response = initiald_schema.dump(cars)
    return jsonify(response)

# delete drone
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_drone(current_user_token, id):
    cars = Initiald.query.get(id)
    db.session.delete(cars)
    db.session.commit()
    response = initiald_schema.dump(cars)
    return jsonify(response)
