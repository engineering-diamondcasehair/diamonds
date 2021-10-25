"""Blueprint for product pages."""
#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from jinja2 import TemplateNotFound
from DiamondCaseWeb.util.gen_util import getCategories
from DiamondCaseWeb.model.product import Product, ProductCategory


blueprint = Blueprint('product', __name__)
db = SQLAlchemy()

@blueprint.route('/category/<int:category_id>')
def category(category_id):
    """View Function for category pages.

    Returns:
        rendered template of view"""
    category = ProductCategory.query.get(category_id)
    return render_template('product-category.html',
        category=category,
        categories=getCategories())

@blueprint.route('/product')
def product():
    """View Function for product pages.

    Returns:
        rendered template of view"""
    products = Product.query.all()
    return render_template('product.html',
        products=products,
        categories=getCategories())

@blueprint.route('/product_highlight/<int:highlight_id>')
def product_highlight(highlight_id):
    """View Function for product pages.
    Args:
        product_id(int): id of product.

    Returns:
        rendered template of view
    """
    return render_template('product_highlight.html',
        categories=getCategories())