#!/usr/bin/python
# -*- coding: utf-8 -*-

from DiamondCaseWeb.model import db


class ProductCategory(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    products = db.relationship('Product', 
        backref='product_category', 
        lazy=True)

    def __init__(self, name):
        self.name = name

    @property
    def serialize(self):
        return {'id': self.id, 'name': self.name}

    def __repr__(self):
        return '<ProductCategory(name=%r)>' % self.name


class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    short_description = db.Column(db.String(80), nullable=False)
    long_description = db.Column(db.Text, nullable=False)
    product_category_id = db.Column(db.Integer, 
        db.ForeignKey('product_category.id'),
        nullable=False)
    img_path_xs = db.Column(db.String(300), nullable=False)
    img_path_sm = db.Column(db.String(300), nullable=False)
    img_path_md = db.Column(db.String(300), nullable=False)
    img_path_lg = db.Column(db.String(300), nullable=False)
    location_products = db.relationship('LocationProduct', 
        backref='product', 
        lazy=True)

    def __init__(
        self,
        name,
        short_description,
        long_description,
        product_category_id,
        img_path_xs,
        img_path_sm,
        img_path_md,
        img_path_lg):
        self.name = name
        self.short_description = short_description
        self.long_description = long_description
        self.product_category_id = product_category_id
        self.img_path_xs = img_path_xs
        self.img_path_sm = img_path_sm
        self.img_path_md = img_path_md
        self.img_path_lg = img_path_lg

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'short_description': self.short_description,
            'long_description': self.long_description,
            'product_category': ProductCategory.query.get(self.product_category_id).serialize,
            'images': {
                'img_path_xs': self.img_path_xs,
                'img_path_sm': self.img_path_sm,
                'img_path_md': self.img_path_md,
                'img_path_lg': self.img_path_lg,
                },
            }

    def __repr__(self):
        return '<Product(name=%r, short_description=%r, long_description=%r, product_category_id=%r, img_path_xs=%r, img_path_sm=%r, img_path_md=%r, img_path_lg=%r)>' % (self.name, self.short_description, self.long_description, self.product_category_id, self.img_path_xs, self.img_path_sm, self.img_path_md, self.img_path_lg)


class Location(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    address1 = db.Column(db.String(120), nullable=False)
    address2 = db.Column(db.String(120))
    city = db.Column(db.String(90), nullable=False)
    state = db.Column(db.String(15), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(60), nullable=False)
    latitude = db.Column(db.Float(precision=10))
    longitude = db.Column(db.Float(precision=10))
    direction_url = db.Column(db.Text, nullable=False)
    location_products = db.relationship('LocationProduct', 
        backref='location', 
        lazy=True)

    def __init__(
        self,
        name,
        description,
        address1,
        address2,
        city,
        state,
        zip_code,
        country,
        latitude,
        longitude,
        direction_url):
        self.name = name
        self.description = description
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
        self.direction_url = direction_url

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'location': {
                'address1': self.address1,
                'address2': self.address2,
                'city': self.city,
                'state': self.state,
                'zip_code': self.zip_code,
                'country': self.country,
                'coordinates': {'latitude': self.latitude,
                                'longitude': self.longitude},
                },
            'direction_url': self.direction_url,
            }

    def __repr__(self):
        return '<Location(name=%r, description=%r, address1=%r, address2=%r, city=%r, state=%r, zip_code=%r, country=%r, latitude=%r, longitude=%r, direction_url=%r)>' % (self.name, self.description, self.address1, self.address2, self.city, self.state, self.zip_code, self.country, self.latitude, self.longitude, self.direction_url)


class LocationProduct(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, 
        db.ForeignKey('location.id'),
        nullable=False)
    product_id = db.Column(db.Integer, 
        db.ForeignKey('product.id'),
        nullable=False)
    price = db.Column(db.Float, nullable=False)
    num_available = db.Column(db.Integer, nullable=False)


    def __init__(
        self,
        location_id,
        product_id,
        price,
        num_available,
        ):
        self.location_id = location_id
        self.product_id = product_id
        self.price = price
        self.num_available = num_available

    @property
    def serialize(self):
        return {
            'id': self.id,
            'location': self.location.serialize,
            'product': self.product.serialize,
            'price': self.price,
            'num_available': self.num_available,
            }

    def __repr__(self):
        return '<LocationProduct(location_id= %r, product_id= %r, price= %r, num_available= %r)>' % (self.location, self.product, self.price, self.num_available)
