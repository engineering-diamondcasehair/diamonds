#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from jinja2 import TemplateNotFound
from DiamondCaseWeb.util.gen_util import getCategories
from DiamondCaseWeb.model.product import Product


blueprint = Blueprint('product', __name__)
db = SQLAlchemy()

@blueprint.route('/product')
def product():
    products = Product.query.all()
    return render_template('product.html',
        products=products,
        categories=getCategories())

@blueprint.route('/product_highlight/<int:id>')
def product_highlight(product_id):
    product = Product.query.get(product_id)
    return render_template('product_highlight.html',
        product=product,
        categories=getCategories())