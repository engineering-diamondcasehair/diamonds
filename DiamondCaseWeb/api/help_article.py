"""API code for Help Articles."""

#!/usr/bin/python
# -*- coding: utf-8 -*-
from DiamondCaseWeb import db
from DiamondCaseWeb.model.static import HelpArticle as HelpArticleModel
from flask import Blueprint
from flask_restful import abort
from flask_restful import Api
from flask_restful import reqparse
from flask_restful import Resource
from flask_restful import url_for

# Register blueprint For help article Api
blueprint = Blueprint('help_article_api', __name__)
api = Api(blueprint)

def abort_if_help_article_doesnt_exist(help_article_id):
    """Checks to see if Help Article record with id={help_article_id} exist, if not the function aborts the requset with 404 status code.

    Args:
        help_article_id(int): Id of help article to retrieve
    """
    if not HelpArticleModel.query.get(help_article_id):
        abort(404,
              message="help_article_id {} doesn't exist".format(help_article_id))


parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('description')
parser.add_argument('body')


class HelpArticle(Resource):
    """Flask-Restful Implementation of API to read, update, and delete Help Article."""
    def get(self, help_article_id):
        """Checks to see if  Help Article record with id={help_article_id} exist, and if so serialize and return it.

        Args:
            help_article_id(int): Id of help article to retrieve.

        Returns:
            Serialized dict/json data containing the information for one article and a status code of 200.
        """
        abort_if_help_article_doesnt_exist(help_article_id)
        article = HelpArticleModel.query.get(help_article_id)
        return article.serialize

    def delete(self, help_article_id):
        """Checks to see if  Help Article record with id={help_article_id} exist, and if so deletes it.

        Args:
            help_article_id(int): Id of help article to retrieve.

        Returns:
            Empty json message and a status code of 204.
        """
        abort_if_help_article_doesnt_exist(help_article_id)
        article = HelpArticleModel.query.get(help_article_id)
        db.session.delete(article)
        db.session.commit()
        return ('', 204)

    def put(self, help_article_id):
        """Checks to see if  Help Article record with id={help_article_id} exist, and if so upadtes it with provided values.

        Args:
            help_article_id(int): Id of help article to retrieve.

        Returns:
            Updated serialized dict/json data containing the information for one article and a status code of 201.
        """
        args = parser.parse_args()
        article = HelpArticleModel.query.get(help_article_id)
        article.title = args['title']
        article.description = args['description']
        article.body = args['body']
        db.session.commit()
        return (article.serialize, 201)


class HelpArticleList(Resource):
    """Flask-Restful Implementation of API to read and create Help Article."""
    def get(self):
        """Retrieve all Help Article records.

        Returns:
            A list of Serialized dict/json data containing the information for one help article each and a status code of 200.
        """
        articles = HelpArticleModel.query.all()
        return [article.serialize for article in articles]

    def post(self):
        """Creates a new Help Article record.

        Returns:
            Serialized dict/json data containing the information for the newly added help article and a status code of 201.
        """
        args = parser.parse_args()
        article = HelpArticleModel(title=args['title'],
                                    description=args['description'],
                                    body=args['body'])
        db.session.add(article)
        db.session.commit()
        return (article.serialize, 201)


api.add_resource(HelpArticleList, '/api/help_articles')
api.add_resource(HelpArticle, '/api/help_article/<help_article_id>')