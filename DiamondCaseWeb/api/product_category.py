"""API code for Product-Category."""

#!/usr/bin/python
# -*- coding: utf-8 -*-
from DiamondCaseWeb import db
from DiamondCaseWeb.model.product import ProductCategory as ProductCategoryModel
from flask import Blueprint
from flask_restful import abort
from flask_restful import Api
from flask_restful import reqparse
from flask_restful import Resource
from flask_restful import url_for
from flask_sqlalchemy import SQLAlchemy

# Register blueprint For product-category Api
blueprint = Blueprint('product_category_api', __name__)
api = Api(blueprint)

def abort_if_product_category_doesnt_exist(product_category_id):
    """Checks to see if Product-Category record with id={product_category_id} exist, if not the function aborts the requset with 404 status code.

    Args:
        product_category_id(int): Id of product-category to retrieve
    """
    if not ProductCategoryModel.query.get(product_category_id):
        abort(404,
              message="product_category_id {} doesn't exist".format(product_category_id))


parser = reqparse.RequestParser()
parser.add_argument('name')


class ProductCategory(Resource):
    """Flask-Restful Implementation of API for ProductCategories."""
    def get(self, product_category_id):
        """Checks to see if Product-Category record with id={product_category_id} exist, and if so serialize and return it.

        Args:
            product_category_id(int): Id of product-category to retrieve.

        Returns:
            Serialized dict/json data containing the information for one product-category and a status code of 200.
        """
        abort_if_product_category_doesnt_exist(product_category_id)
        category = ProductCategoryModel.query.get(product_category_id)
        return category.serialize

    def delete(self, product_category_id):
        """Checks to see if  Product-Category record with id={product_category_id} exist, and if so deletes it.

        Args:
            product_category_id(int): Id of product-category to retrieve.

        Returns:
            Empty json message and a status code of 204.
        """
        abort_if_product_category_doesnt_exist(product_category_id)
        category = ProductCategoryModel.query.get(product_category_id)
        db.session.delete(category)
        db.session.commit()
        return ('', 204)

    def put(self, product_category_id):
        """Checks to see if Product-Category record with id={product_category_id} exist, and if so upadtes it with provided values.

        Args:
            product_category_id(int): Id oflocation to retrieve.

        Returns:
            Updated serialized dict/json data containing the information for one product_category and a status code of 201.
        """
        args = parser.parse_args()
        category = ProductCategoryModel.query.get(product_category_id)
        category.name = args['name']
        db.session.commit()
        return (category.serialize, 201)


class ProductCategoryList(Resource):
    """Flask-Restful Implementation of API to read and create ProductCategory."""
    def get(self):
        """Retrieve all Product-Categories records.

        Returns:
            A list of Serialized dict/json data containing the information for one location each and a status code of 200.
        """
        categories = ProductCategoryModel.query.all()
        return [category.serialize for category in categories]

    def post(self):
        """Creates a new Product-Category record.

        Returns:
            Serialized dict/json data containing the information for the newly added product-category and a status code of 201.
        """
        args = parser.parse_args()
        category = ProductCategoryModel(name=args['name'])
        db.session.add(category)
        db.session.commit()
        return (category.serialize, 201)


api.add_resource(ProductCategoryList, '/api/product_categories')
api.add_resource(ProductCategory,
                 '/api/product_category/<int:product_category_id>')
