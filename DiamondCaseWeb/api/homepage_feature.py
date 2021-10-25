"""API code for Homepage Features."""

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

# Register blueprint For help article Api
blueprint = Blueprint('homepagefeature_api', __name__)
api = Api(blueprint)

def abort_if_homepage_features_doesnt_exist(homepage_feature_id):
    """Checks to see if Homepage Features record with id={homepage_feature_id} exist, if not the function aborts the requset with 404 status code.

    Args:
        homepage_feature_id(int): Id of homepage feature to retrieve
    """
    if not HomepageFeatureModel.query.get(homepage_features_id):
        abort(404,
              message="homepage_features_id {} doesn't exist".format(homepage_feature_id))


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
    """Flask-Restful Implementation of API for Homepage Features."""
    def get(self, homepage_feature_id):
        """Checks to see if  Homepage Feature record with id={help_article_id} exist, and if so serialize and return it.

        Args:
            homepage_feature_id(int): Id of help article to retrieve.

        Returns:
            Serialized dict/json data containing the information for one article and a status code of 200.
        """
        abort_if_homepage_features_doesnt_exist(homepage_feature_id)
        feature = HomepageFeatureModel.query.get(homepage_feature_id)
        return feature.serialize

    def delete(self, homepage_feature_id):
        """Checks to see if  Homepage Feature record with id={homepage_feature_id} exist, and if so deletes it.

        Args:
            homepage_feature_id(int): Id of homepage feature to retrieve.

        Returns:
            Empty json message and a status code of 204.
        """
        abort_if_homepage_features_doesnt_exist(homepage_feature_id)
        feature = HomepageFeatureModel.query.get(homepage_feature_id)
        db.session.delete(feature)
        db.session.commit()
        return ('', 204)

    def put(self, homepage_feature_id):
        """Checks to see if  Homepage Feature record with id={homepage_feature_id} exist, and if so upadtes it with provided values.

        Args:
            homepage_feature_id(int): Id of homepage feature to retrieve.

        Returns:
            Updated serialized dict/json data containing the information for one homepage feature and a status code of 201.
        """
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
        """Retrieve all Homepage Feature records.

        Returns:
            A list of serialized dict/json data containing the information for one homepage Feature each and a status code of 200.
        """
        features = HomepageFeatureModel.query.all()
        return [feature.serialize for feature in features]

    def post(self):
        """Creates a new Homepage Feature record.

        Returns:
            Serialized dict/json data containing the information for the newly added Homepage Feature and a status code of 201.
        """
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
