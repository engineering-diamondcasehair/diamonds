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

blueprint = Blueprint('product_category_api', __name__)
api = Api(blueprint)

def abort_if_product_category_doesnt_exist(product_category_id):
    if not ProductCategoryModel.query.get(product_category_id):
        abort(404,
              message="product_category_id {} doesn't exist".format(product_category_id))


parser = reqparse.RequestParser()
parser.add_argument('name')


class ProductCategory(Resource):

    def get(self, product_category_id):
        abort_if_product_category_doesnt_exist(product_category_id)
        category = ProductCategoryModel.query.get(product_category_id)
        return category.serialize

    def delete(self, product_category_id):
        abort_if_product_category_doesnt_exist(product_category_id)
        category = ProductCategoryModel.query.get(product_category_id)
        db.session.delete(category)
        db.session.commit()
        return ('', 204)

    def put(self, product_category_id):
        args = parser.parse_args()
        category = ProductCategoryModel.query.get(product_category_id)
        category.name = args['name']
        db.session.commit()
        return (category.serialize, 201)


class ProductCategoryList(Resource):

    def get(self):
        categories = ProductCategoryModel.query.all()
        return [category.serialize for category in categories]

    def post(self):
        args = parser.parse_args()
        category = ProductCategoryModel(name=args['name'])
        db.session.add(category)
        db.session.commit()
        return (category.serialize, 201)


api.add_resource(ProductCategoryList, '/api/product_categories')
api.add_resource(ProductCategory,
                 '/api/product_category/<int:product_category_id>')
