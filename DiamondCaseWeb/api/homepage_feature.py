#!/usr/bin/python
# -*- coding: utf-8 -*-
from DiamondCaseWeb import db
from DiamondCaseWeb.model.static import HomepageFeature as HomepageFeatureModel
from flask import Blueprint
from flask_restful import abort
from flask_restful import Api
from flask_restful import reqparse
from flask_restful import Resource
from flask_restful import url_for

blueprint = Blueprint('homepagefeature_api', __name__)
api = Api(blueprint)

def abort_if_homepage_features_doesnt_exist(homepage_features_id):
    if not HomepageFeatureModel.query.get(homepage_features_id):
        abort(404,
              message="homepage_features_id {} doesn't exist".format(homepage_features_id))


parser = reqparse.RequestParser()
parser.add_argument('title', 
    type=str, 
    location='json', 
    required=True)
parser.add_argument('body', 
    type=str, 
    location='json', 
    required=True)
parser.add_argument('img_path_xs',
    type=str,
    location='json',
    required=True)
parser.add_argument('img_path_sm', 
    type=str, 
    location='json', 
    required=True)
parser.add_argument('img_path_md', 
    type=str, 
    location='json', 
    required=True)
parser.add_argument('img_path_lg', 
    type=str, 
    location='json', 
    required=True)
parser.add_argument('is_active', 
    type=bool, 
    location='json', 
    required=True)


class HomepageFeature(Resource):

    def get(self, homepage_feature_id):
        abort_if_homepage_features_doesnt_exist(homepage_feature_id)
        feature = HomepageFeatureModel.query.get(homepage_feature_id)
        return feature.serialize

    def delete(self, homepage_feature_id):
        abort_if_homepage_features_doesnt_exist(homepage_feature_id)
        feature = HomepageFeatureModel.query.get(homepage_feature_id)
        db.session.delete(feature)
        db.session.commit()
        return ('', 204)

    def put(self, homepage_feature_id):
        args = parser.parse_args()
        feature = HomepageFeatureModel.query.get(homepage_feature_id)
        feature.title = args['title']
        feature.body = args['body']
        feature.img_path_xs = args['img_path_xs']
        feature.img_path_sm = args['img_path_sm']
        feature.img_path_md = args['img_path_md']
        feature.img_path_lg = args['img_path_lg']
        feature.is_active = args['is_active']
        db.session.commit()
        return (feature.serialize, 201)


class HomepageFeatureList(Resource):

    def get(self):
        features = HomepageFeatureModel.query.all()
        return [feature.serialize for feature in features]

    def post(self):
        args = parser.parse_args()
        feature = HomepageFeatureModel(
            title=args['title'],
            body=args['body'],
            img_path_xs=args['img_path_xs'],
            img_path_sm=args['img_path_sm'],
            img_path_md=args['img_path_md'],
            img_path_lg=args['img_path_lg'],
            is_active=args['is_active'])
        db.session.add(feature)
        db.session.commit()
        return (feature.serialize, 201)


api.add_resource(HomepageFeatureList, '/api/homepage_features')
api.add_resource(HomepageFeature,
                 '/api/homepage_feature/<homepage_feature_id>')
