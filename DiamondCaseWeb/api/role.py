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

blueprint = Blueprint('role_api', __name__)
api = Api(blueprint)

def abort_if_role_doesnt_exist(role_id):
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
    def get(self, role_id):
        abort_if_role_doesnt_exist(role_id)
        role = RoleModel.query.get(role_id)
        return role.serialize

    def delete(self, role_id):
        abort_if_role_doesnt_exist(role_id)
        role = RoleModel.query.get(role_id)
        db.session.delete(role)
        db.session.commit()
        return ('', 204)

    def put(self, role_id):
        abort_if_role_doesnt_exist(role_id)
        args = parser.parse_args()
        role = RoleModel.query.get(role_id)
        role.name = args['name']
        role.description = args['description']
        db.session.commit()
        return (role.serialize, 201)


class RoleList(Resource):

    def get(self):
        roles = RoleModel.query.all()
        return [role.serialize for role in roles]

    def post(self):
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
