#!/usr/bin/python
# -*- coding: utf-8 -*-
from DiamondCaseWeb import db
from DiamondCaseWeb.model.product import Location as LocationModel
from flask import Blueprint
from flask_restful import abort
from flask_restful import Api
from flask_restful import reqparse
from flask_restful import Resource
from flask_restful import url_for

blueprint = Blueprint('location_api', __name__)
api = Api(blueprint)

def abort_if_location_doesnt_exist(location_id):
    if not LocationModel.query.get(location_id):
        abort(404,
              message="location_id {} doesn't exist".format(location_id))


parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('description')
parser.add_argument('address1')
parser.add_argument('address2')
parser.add_argument('city')
parser.add_argument('state')
parser.add_argument('zip_code')
parser.add_argument('country')
parser.add_argument('latitude')
parser.add_argument('longitude')
parser.add_argument('direction_url')


class Location(Resource):

    def get(self, location_id):
        abort_if_location_doesnt_exist(location_id)
        location = LocationModel.query.get(location_id)
        return location.serialize

    def delete(self, location_id):
        abort_if_location_doesnt_exist(location_id)
        location = LocationModel.query.get(location_id)
        db.session.delete(location)
        db.session.commit()
        return ('', 204)

    def put(self, location_id):
        args = parser.parse_args()
        location = LocationModel.query.get(location_id)
        location.name = args['name']
        location.description = args['description']
        location.address1 = args['address1']
        location.address2 = args['address2']
        location.city = args['city']
        location.zip_code = args['zip_code']
        location.state = args['state']
        location.country = args['country']
        location.latitude = args['latitude']
        location.longitude = args['longitude']
        location.direction_url = args['direction_url']
        db.session.commit()
        return (location.serialize, 201)


class LocationList(Resource):

    def get(self):
        locations = LocationModel.query.all()
        return [location.serialize for location in locations]

    def post(self):
        args = parser.parse_args()
        location = LocationModel(
            name=args['name'],
            description=args['description'],
            address1=args['address1'],
            address2=args['address2'],
            city=args['city'],
            state=args['state'],
            zip_code=args['zip_code'],
            country=args['country'],
            latitude=args['latitude'],
            longitude=args['longitude'],
            direction_url=args['direction_url'])
        db.session.add(location)
        db.session.commit()
        return (location.serialize, 201)


api.add_resource(LocationList, '/api/locations')
api.add_resource(Location, '/api/location/<int:location_id>')
