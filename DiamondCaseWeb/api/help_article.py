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

blueprint = Blueprint('help_article_api', __name__)
api = Api(blueprint)

def abort_if_help_article_doesnt_exist(help_article_id):
    if not HelpArticleModel.query.get(help_article_id):
        abort(404,
              message="help_article_id {} doesn't exist".format(help_article_id))


parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('description')
parser.add_argument('body')


class HelpArticle(Resource):

    def get(self, help_article_id):
        abort_if_help_article_doesnt_exist(help_article_id)
        article = HelpArticleModel.query.get(help_article_id)
        return article.serialize

    def delete(self, help_article_id):
        abort_if_help_article_doesnt_exist(help_article_id)
        article = HelpArticleModel.query.get(help_article_id)
        db.session.delete(article)
        db.session.commit()
        return ('', 204)

    def put(self, help_article_id):
        args = parser.parse_args()
        article = HelpArticleModel.query.get(help_article_id)
        article.title = args['title']
        article.description = args['description']
        article.body = args['body']
        db.session.commit()
        return (article.serialize, 201)


class HelpArticleList(Resource):

    def get(self):
        articles = HelpArticleModel.query.all()
        return [article.serialize for article in articles]

    def post(self):
        args = parser.parse_args()
        article = HelpArticleModel(title=args['title'],
                                    description=args['description'],
                                    body=args['body'])
        db.session.add(article)
        db.session.commit()
        return (article.serialize, 201)


api.add_resource(HelpArticleList, '/api/help_articles')
api.add_resource(HelpArticle, '/api/help_article/<help_article_id>')
