"""Blueprint for shop pages."""
#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from DiamondCaseWeb.model.product import Location
from flask import Blueprint, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from jinja2 import TemplateNotFound
from DiamondCaseWeb.util.gen_util import getCategories


blueprint = Blueprint('shop', __name__)
db = SQLAlchemy()

@blueprint.route('/locator')
def locator():
    """View Function for locator pages.

    Returns:
        rendered template of view
    """
    locations = Location.query.all()
    return render_template('locator.html', locations=locations,
        categories=getCategories(), json_data=json.dumps([location.serialize for location in locations]))


@blueprint.route('/shop/<int:machine_id>')
def machine(machine_id):
    """View Function for machine pages.

    Args:
        machine_id(int): id of machine.

    Returns:
        rendered template of view
    """
    location = Location.query.get(machine_id)
    return render_template('machine-product.html',
                           machine_id=machine_id, location=location, categories=getCategories())

@blueprint.route('/cart')
def cart():
    """View Function for cart pages.

    Returns:
        rendered template of view
    """
    def getIser():
        """Returns active user."""
        return ['','']
    cart = Cart.query.filter(user=getIser(), active=true).all()
    return render_template('cart.html', data=data, categories=getCategories())


@blueprint.route('/checkout')
def checkout():
    """View Function for checkout pages.

    Returns:
        rendered template of view
    """
    def getUser():
        """Returns active user."""
        return 1
    cart = Cart.query.filter(user_id=getUser(), active=true).all()
    return render_template('checkout.html', cart=cart, categories=getCategories())
