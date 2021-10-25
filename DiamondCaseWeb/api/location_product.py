"""API code for Location-Products."""

#!/usr/bin/python
# -*- coding: utf-8 -*-
from DiamondCaseWeb import db
from DiamondCaseWeb.model.product import Product as ProductModel
from DiamondCaseWeb.model.product import Location as LocationModel
from DiamondCaseWeb.model.product import LocationProduct as LocationProductModel
from flask import Blueprint
from flask_restful import abort
from flask_restful import Api
from flask_restful import reqparse
from flask_restful import Resource
from flask_restful import url_for

# Register blueprint For Location-Product Api
blueprint = Blueprint('location_product_api', __name__)
api = Api(blueprint)

def abort_if_location_product_doesnt_exist(location_product_id):
    """Checks to see if Location-Product record with id={location_product_id} exist, if not the function aborts the requset with 404 status code.

    Args:
        location_id(int): Id of location to retrieve
    """
    if not LocationProductModel.query.get(location_product_id):
        abort(404,
              message="location_product_id {} doesn't exist".format(location_product_id))


parser = reqparse.RequestParser()
parser.add_argument('location_id')
parser.add_argument('product_id')
parser.add_argument('price')
parser.add_argument('num_available')


class LocationProduct(Resource):
    """Flask-Restful Implementation of API for Location-Products."""
    def get(self, location_product_id):
        """Checks to see if  Location-Product record with id={location_product_id} exist, and if so serialize and return it.

        Args:
            location_product_id(int): Id of location-product to retrieve.

        Returns:
            Serialized dict/json data containing the information for one location-product and a status code of 200.
        """
        abort_if_location_product_doesnt_exist(location_product_id)
        location_product = \
            LocationProductModel.query.get(location_product_id)
        return location_product.serialize

    def delete(self, location_product_id):
        """Checks to see if  Location-Product record with id={location_product_id} exist, and if so deletes it.

        Args:
            location_product_id(int): Id of location-product to retrieve.

        Returns:
            Empty json message and a status code of 204.
        """
        abort_if_location_product_doesnt_exist(location_product_id)
        location_product = LocationProductModel.query.get(location_product_id)
        db.session.delete(location_product)
        db.session.commit()
        return ('', 204)

    def put(self, location_product_id):
        """Checks to see if Location-Product record with id={location_product_id} exist, and if so upadtes it with provided values.

        Args:
            location_product_id(int): Id oflocation-product to retrieve.

        Returns:
            Updated serialized dict/json data containing the information for one location-product and a status code of 201.
        """
        args = parser.parse_args()
        location_product = \
            LocationProductModel.query.get(location_product_id)
        location_product.location_id = args['location_id']
        location_product.product_id = args['product_id']
        location_product.price = args['price']
        location_product.num_available = args['num_available']
        db.session.commit()
        return (location_product.serialize, 201)


class LocationProductList(Resource):
    """Flask-Restful Implementation of API to read and create Location-Product."""
    def get(self):
        """Retrieve all Location-Product records.

        Returns:
            A list of Serialized dict/json data containing the information for one location-product each and a status code of 200.
        """
        location_products = LocationProductModel.query.all()
        return [location_product.serialize for location_product in
                location_products]

    def post(self):
        """Creates a new Location-Product record.

        Returns:
            Serialized dict/json data containing the information for the newly added location-product and a status code of 201.
        """
        args = parser.parse_args()
        location_product = LocationProductModel(
            location_id=args['location_id'],
            product_id=args['product_id'], 
            price=args['price'],
            num_available=args['num_available'])
        db.session.add(location_product)
        db.session.commit()
        return (location_product.serialize, 201)


api.add_resource(LocationProductList, '/api/location_products')
api.add_resource(LocationProduct,
                 '/api/location_product/<location_product_id>')
