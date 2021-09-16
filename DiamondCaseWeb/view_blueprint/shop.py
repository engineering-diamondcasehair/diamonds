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
    locations = Location.query.all()
    return render_template('locator.html', locations=locations,
        categories=getCategories())


@blueprint.route('/shop/<int:machine_id>')
def machine(machine_id):
    location = Location.query.get(machine_id)
    return render_template('machine-product.html',
                           machine_id=machine_id, location=location, categories=getCategories())


@blueprint.route('/cart')
def cart():
    def getIser():
        return ['','']
    cart = Cart.query.filter(user=getIser(), active=true).all()
    return render_template('cart.html', data=data, categories=getCategories())


@blueprint.route('/checkout')
def checkout():
    def getUser():
        return 1
    cart = Cart.query.filter(user_id=getUser(), active=true).all()
    return render_template('checkout.html', cart=cart, categories=getCategories())
