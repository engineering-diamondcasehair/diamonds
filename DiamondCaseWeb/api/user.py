"""API code for Users."""

#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
from DiamondCaseWeb import db
from DiamondCaseWeb.model.user import User as UserModel
from flask import Blueprint
from flask_restful import abort
from flask_restful import Api
from flask_restful import reqparse
from flask_restful import Resource
from flask_restful import url_for
from dateutil import parser as date_parser

# Register blueprint For user Api
blueprint = Blueprint('user_api', __name__)
api = Api(blueprint)

def abort_if_user_doesnt_exist(user_id):
    """Checks to see if User record with id={user_id} exist, if not the function aborts the requset with 404 status code.

    Args:
        location_id(int): Id of location to retrieve
    """
    if not UserModel.query.get(user_id):
        abort(404,
              message="user_id {} doesn't exist".format(user_id))


parser = reqparse.RequestParser()
parser.add_argument('name', 
    type=str, 
    location='json', 
    required=True)
parser.add_argument('phone', 
    type=str, 
    location='json', 
    required=True)
parser.add_argument('email', 
    type=str, 
    location='json', 
    required=True)
parser.add_argument('password', 
    type=str, 
    location='json', 
    required=False)
parser.add_argument('salted_hashed_password', 
    type=str, 
    location='json', 
    required=False)
parser.add_argument('confirmed_at', 
    type=str, 
    location='json', 
    required=True)
parser.add_argument('role_id', 
    type=int, 
    location='json', 
    required=True)
parser.add_argument('active', 
    type=bool, 
    location='json', 
    required=False)
parser.add_argument('banned', 
    type=bool, 
    location='json', 
    required=False)


class User(Resource):
    """Flask-Restful Implementation of API for Users."""
    def get(self, user_id):
        """Checks to see if User record with id={user_id} exist, and if so serialize and return it.

        Args:
            user_id(int): Id of user to retrieve.

        Returns:
            Serialized dict/json data containing the information for one location and a status code of 200.
        """
        abort_if_user_doesnt_exist(user_id)
        user = UserModel.query.get(user_id)
        return user.serialize

    def delete(self, user_id):
        """Checks to see if  User record with id={user_id} exist, and if so deletes it.

        Args:
            user_id(int): Id of user to retrieve.

        Returns:
            Empty json message and a status code of 204.
        """
        abort_if_user_doesnt_exist(user_id)
        user = UserModel.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return ('', 204)

    def put(self, user_id):
        """Checks to see if User record with id={user_id} exist, and if so upadtes it with provided values.

        Args:
            user_id(int): Id of user to retrieve.

        Returns:
            Updated serialized dict/json data containing the information for one user and a status code of 201.
        """
        abort_if_user_doesnt_exist(user_id)
        args = parser.parse_args()
        if bool(args['salted_hashed_password']) == bool(args['password']):
	        abort(404,
	              message="Inconsistant Password Request. Contact {}".format('email@example.com'))
        user = UserModel.query.get(user_id)
        user.name = args['name']
        user.phone = args['phone']
        user.email = args['email']
        if not args['salted_hashed_password']:
        	user.salted_hashed_password = user.salt_and_hash(args['password'])
        else:
        	user.salted_hashed_password = args['salted_hashed_password']
        user.active = args['active']
        user.banned = args['banned']
        user.confirmed_at = date_parser.parse(args['confirmed_at'])
        user.role_id = args['role_id']
        db.session.commit()
        return (user.serialize, 201)


class UserList(Resource):
    """Flask-Restful Implementation of API to read and create User."""
    def get(self):
        """Retrieve all User records.

        Returns:
            A list of Serialized dict/json data containing the information for one user each and a status code of 200.
        """
        users = UserModel.query.all()
        return [user.serialize for user in users]

    def post(self):
        """Creates a new User record.

        Returns:
            Serialized dict/json data containing the information for the newly added user and a status code of 201.
        """
        args = parser.parse_args()
        user = UserModel(
	        name=args['name'],
	        phone=args['phone'],
	        email=args['email'],
	        password=args['password'],
	        confirmed_at=date_parser.parse(args['confirmed_at']),
	        role_id=args['role_id'])
        db.session.add(user)
        db.session.commit()
        return (user.serialize, 201)

api.add_resource(UserList, '/api/users')
api.add_resource(User,
                 '/api/user/<int:user_id>')