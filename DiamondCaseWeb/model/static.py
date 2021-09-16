#!/usr/bin/python
# -*- coding: utf-8 -*-

from DiamondCaseWeb.model import db

class HomepageFeature(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_path_xs = db.Column(db.String(300), nullable=False)
    img_path_sm = db.Column(db.String(300), nullable=False)
    img_path_md = db.Column(db.String(300), nullable=False)
    img_path_lg = db.Column(db.String(300), nullable=False)
    is_active = db.Column(db.Boolean, unique=False, default=False)

    def __init__(
        self,
        title,
        body,
        img_path_xs,
        img_path_sm,
        img_path_md,
        img_path_lg,
        is_active):
        self.title = title
        self.body = body
        self.img_path_xs = img_path_xs
        self.img_path_sm = img_path_sm
        self.img_path_md = img_path_md
        self.img_path_lg = img_path_lg
        self.is_active = is_active

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'images': {
                'img_path_xs': self.img_path_xs,
                'img_path_sm': self.img_path_sm,
                'img_path_md': self.img_path_md,
                'img_path_lg': self.img_path_lg
            },
            'is_active': self.is_active,
            }

    def __repr__(self):
        return '<HomepageFeatures(title=%r, body=%r, img_path_xs=%r, img_path_sm=%r, img_path_md=%r, img_path_lg=%r, is_active=%r)>' % (self.title, self.body, self.img_path_xs, self.img_path_sm, self.img_path_md, self.img_path_lg, self.is_active)


class HelpArticle(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    body = db.Column(db.Text, nullable=False)

    def __init__(
        self,
        title,
        description,
        body):
        self.title = title
        self.description = description
        self.body = body

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'body': self.body,
            }

    def __repr__(self):
        return '<HelpArticle(title=%r, description=%r, body=%r)>' % (self.title, self.description, self.body)
