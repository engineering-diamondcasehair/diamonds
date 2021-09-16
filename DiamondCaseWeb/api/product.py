#!/usr/bin/python
# -*- coding: utf-8 -*-
from DiamondCaseWeb import db
from DiamondCaseWeb.model.product import Product as ProductModel
from flask import Blueprint
from flask_restful import abort
from flask_restful import Api
from flask_restful import reqparse
from flask_restful import Resource
from flask_restful import url_for

blueprint = Blueprint('bproduct_api', __name__)
api = Api(blueprint)

def abort_if_product_doesnt_exist(product_id):
    if not ProductModel.query.get(product_id):
        abort(404, message="Product {} doesn't exist".format(product_id))


parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('short_description')
parser.add_argument('long_description')
parser.add_argument('product_category_id')
parser.add_argument('img_path_xs')
parser.add_argument('img_path_sm')
parser.add_argument('img_path_md')
parser.add_argument('img_path_lg')


class Product(Resource):

    def get(self, product_id):
        abort_if_product_doesnt_exist(product_id)
        product = ProductModel.query.get(product_id)
        return product.serialize

    def delete(self, product_id):
        abort_if_product_doesnt_exist(product_id)
        product = ProductModel.query.get(product_id)
        db.session.delete(product)
        db.session.commit()
        return ('', 204)

    def put(self, product_id):
        args = parser.parse_args()
        product = ProductModel.query.get(product_id)
        product.name = args['name']
        product.short_description = args['short_description']
        product.long_description = args['long_description']
        product.product_category_id = args['product_category_id']
        product.img_path_xs = args['img_path_xs']
        product.img_path_sm = args['img_path_sm']
        product.img_path_md = args['img_path_md']
        product.img_path_lg = args['img_path_lg']
        db.session.commit()
        return (product.serialize, 201)


class ProductList(Resource):

    def get(self):
        products = ProductModel.query.all()
        return [product.serialize for product in products]

    def post(self):
        args = parser.parse_args()
        product = ProductModel(
            name=args['name'],
            short_description=args['short_description'],
            long_description=args['long_description'],
            product_category_id=args['product_category_id'],
            img_path_xs=args['img_path_xs'],
            img_path_sm=args['img_path_sm'],
            img_path_md=args['img_path_md'],
            img_path_lg=args['img_path_lg']
            )
        db.session.add(product)
        db.session.commit()
        return (product.serialize, 201)


api.add_resource(ProductList, '/api/products')
api.add_resource(Product, '/api/product/<product_id>')
