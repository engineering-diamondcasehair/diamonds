#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
from DiamondCaseWeb.model import db
import hashlib
from .product import LocationProduct

# Order Model
class Order(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    active = db.Column(db.Boolean, default=True)
    purchase_timestamp = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, 
        db.ForeignKey('user.id'),
        nullable=False)
    product_location_id = db.Column(db.Integer, 
        db.ForeignKey('LocationProduct.id'),
        nullable=False)


# Role Model
class Role(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    users = db.relationship('User', 
        backref='role', 
        lazy=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @property
    def serialize(self):
        return {'id': self.id, 
        'name': self.name,
        'description': self.description
    }

    def __repr__(self):
        return '<HomepageFeatures(title=%r, body=%r, img_path_xs=%r, img_path_sm=%r, img_path_md=%r, img_path_lg=%r, is_active=%r)>' % (self.title, self.body, self.img_path_xs, self.img_path_sm, self.img_path_md, self.img_path_lg, self.is_active)


# User Model
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(13), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    salted_hashed_password = db.Column(db.String(120), unique=True,
            nullable=False)
    active = db.Column(db.Boolean, default=False)
    banned = db.Column(db.Boolean, default=False)
    confirmed_at = db.Column(db.DateTime())
    role_id = db.Column(db.Integer, 
        db.ForeignKey('role.id'),
        nullable=False)
    orders = db.relationship('Order', 
        backref='user', 
        lazy=True)
   
    def __init__(
        self,
        name,
        phone,
        email,
        password,
        confirmed_at,
        role_id):
        self.name = name
        self.phone = phone
        self.email = email
        self.salt = datetime.datetime.now().isoformat()
        self.salted_hashed_password = self.salt_and_hash(password)
        self.confirmed_at = confirmed_at
        self.role_id = role_id

    @property
    def serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'salted_hashed_password': self.salted_hashed_password,
            'active': self.active,
            'banned': self.banned,
            'confirmed_at': self.confirmed_at.isoformat(),
            'role': Role.query.get(self.role_id).serialize
        }

    def salt_and_hash(self, password):
        db_password = password + self.salt
        h = hashlib.md5(db_password.encode())
        return h.hexdigest()