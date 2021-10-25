"""Set up database Schema for User Related database tables."""
#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
from DiamondCaseWeb.model import db
import hashlib
from .product import LocationProduct

# Order Model
# class Order(db.Model):
#     """Set database model for Order."""

#     id = db.Column(db.Integer(), primary_key=True)
#     active = db.Column(db.Boolean, default=True)
#     purchase_timestamp = db.Column(db.DateTime())
#     user_id = db.Column(db.Integer, 
#         db.ForeignKey('user.id'),
#         nullable=False)
#     product_location_id = db.Column(db.Integer, 
#         db.ForeignKey('LocationProduct.id'),
#         nullable=False)

#     def __init__(self, active, user_id, product_location_id):
#         """Creates a Order record.
        
#         Args:
#             active(bool): Is order item in an active status.
#             user_id(int): ForeignKey that associates order with User.
#             product_location_id(int): ForeignKey that associates order with Product-Location.
#         """
#         self.name = name
#         self.description = description

#     @property
#     def serialize(self):
#         """Creates string representation of how to create this Role record.
        
#         Returns:
#             Returns JSON dictionary of Role record."
#         """
#         return {'id': self.id, 
#         'name': self.name,
#         'description': self.description
#     }

#     def __repr__(self):
#         """Creates string representation of how to create this Role record.
        
#         Returns:
#             String containing initialization function for this record.
#         """
#         return '<Role(name=%r, description=%r)>' % (self.name, self.description)


# Role Model
class Role(db.Model):
    """Set database model for Role."""

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    users = db.relationship('User', 
        backref='role', 
        lazy=True)

    def __init__(self, name, description):
        """Creates a Role record.
        
        Args:
            name(str): Name of Role.
            description(str): Description of Role.
        """
        self.name = name
        self.description = description

    @property
    def serialize(self):
        """Creates string representation of how to create this Role record.
        
        Returns:
            Returns JSON dictionary of Role record."
        """
        return {'id': self.id, 
        'name': self.name,
        'description': self.description
    }

    def __repr__(self):
        """Creates string representation of how to create this Role record.
        
        Returns:
            String containing initialization function for this record.
        """
        return '<Role(name=%r, description=%r)>' % (self.name, self.description)


# User Model
class User(db.Model):
    """Set database model for User."""

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
    # orders = db.relationship('Order', 
    #     backref='user', 
    #     lazy=True)
   
    def __init__(
        self,
        name,
        phone,
        email,
        password,
        confirmed_at,
        role_id):
        """Creates a User record.
        
        Args:
            name(str): Name of User.
            phone(str): Phone Nuber of User.
            email(str): Email adress of User.
            password(str): Plain text password entered by user.
            confirmed_at(db.DateTime): Datetime of last user interaction.
            role_id(int): Primary key of associated role(customer/admin).
        """
        self.name = name
        self.phone = phone
        self.email = email
        self.salt = datetime.datetime.now().isoformat()
        self.salted_hashed_password = self.salt_and_hash(password)
        self.confirmed_at = confirmed_at
        self.role_id = role_id

    @property
    def serialize(self):
        """Creates string representation of how to create this User record.
        
        Returns:
            Returns JSON dictionary of User record."
        """
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

    def __repr__(self):
        """Creates string representation of how to create this User record.
        
        Returns:
            String containing initialization function for this record.
        """
        return '<User(name=%r, phone=%r, email=%r, salted_hashed_password=%r, active=%r, banned=%r, confirmed_at=%r, role_id=%r)>' % (self.name, self.phone, self.email, self.salted_hashed_password, self.active, self.banned, self.confirmed_at.isoformat(), self.role_id)

    def salt_and_hash(self, password):
        """Salt password with datetme of account creation and apply md5 hash.

        Args:
            password(str): Plain text password;password provided by user.

        Returns:
            hex of salted and hashed password.
        """
        db_password = password + self.salt
        h = hashlib.md5(db_password.encode())
        return h.hexdigest()