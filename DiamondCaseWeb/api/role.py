"""API code for Role."""

#!/usr/bin/python
# -*- coding: utf-8 -*-
from DiamondCaseWeb import db
from DiamondCaseWeb.model.user import Role as RoleModel

from flask import Blueprint
from flask_restful import abort
from flask_restful import Api
from flask_restful import reqparse
from flask_restful import Resource
from flask_restful import url_for

# Register blueprint For user Api
blueprint = Blueprint('role_api', __name__)
api = Api(blueprint)

def abort_if_role_doesnt_exist(role_id):
    """Checks to see if Role record with id={role_id} exist, if not the function aborts the requset with 404 status code.

    Args:
        role_id(int): Id of role to retrieve
    """
    if not RoleModel.query.get(role_id):
        abort(404,
              message="role_id {} doesn't exist".format(role_id))


parser = reqparse.RequestParser()
parser.add_argument('name', 
    type=str, 
    location='json', 
    required=True)
parser.add_argument('description', 
    type=str, 
    location='json', 
    required=True)


class Role(Resource):
    """Flask-Restful Implementation of API for Roles."""
    def get(self, role_id):
        """Checks to see if Role record with id={role_id} exist, and if so serialize and return it.

        Args:
            location_id(int): Id of location to retrieve.

        Returns:
            Serialized dict/json data containing the information for one location and a status code of 200.
        """
        abort_if_role_doesnt_exist(role_id)
        role = RoleModel.query.get(role_id)
        return role.serialize

    def delete(self, role_id):
        """Checks to see if Role record with id={role_id} exist, and if so deletes it.

        Args:
            role_id(int): Id of role to retrieve.

        Returns:
            Empty json message and a status code of 204.
        """
        abort_if_role_doesnt_exist(role_id)
        role = RoleModel.query.get(role_id)
        db.session.delete(role)
        db.session.commit()
        return ('', 204)

    def put(self, role_id):
        """Checks to see if Role record with id={role_id} exist, and if so upadtes it with provided values.

        Args:
            role_id(int): Id of role to retrieve.

        Returns:
            Updated serialized dict/json data containing the information for one role and a status code of 201.
        """
        abort_if_role_doesnt_exist(role_id)
        args = parser.parse_args()
        role = RoleModel.query.get(role_id)
        role.name = args['name']
        role.description = args['description']
        db.session.commit()
        return (role.serialize, 201)


class RoleList(Resource):
    """Flask-Restful Implementation of API to read and create User."""
    def get(self):
        """Retrieve all Role records.

        Returns:
            A list of Serialized dict/json data containing the information for one role each and a status code of 200.
        """
        roles = RoleModel.query.all()
        return [role.serialize for role in roles]

    def post(self):
        """Creates a new Role record.

        Returns:
            Serialized dict/json data containing the information for the newly added role and a status code of 201.
        """
        args = parser.parse_args()
        role = RoleModel(
            name=args['name'],
            description=args['description'],)
        db.session.add(role)
        db.session.commit()
        return (role.serialize, 201)


api.add_resource(RoleList, '/api/roles')
api.add_resource(Role,
                 '/api/role/<int:role_id>')
