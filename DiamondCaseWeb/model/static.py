"""Set up database Schema for Static Related database tables."""

#!/usr/bin/python
# -*- coding: utf-8 -*-

from DiamondCaseWeb.model import db

class HomepageFeature(db.Model):
    """Set database model for Homepage-Feature."""

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
        """Creates a Homepage-Feature record.
        
        Args:
            title(str): Title of Homepage Feature.
            body(str): Body text for Homepage Feature.
            img_path_xs(str): Path extra small image.
            img_path_sm(str): Path small image.
            img_path_md(str): Path medium image.
            img_path_lg(str): Path large image.
            is_active(bool): Is homepage feature active..
        """

        self.title = title
        self.body = body
        self.img_path_xs = img_path_xs
        self.img_path_sm = img_path_sm
        self.img_path_md = img_path_md
        self.img_path_lg = img_path_lg
        self.is_active = is_active

    @property
    def serialize(self):
        """Serializzes a Homepage-Feature record.
        
        Returns:
            Returns JSON dictionary of Homepage-Feature record.
        """
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
        """Creates string representation of how to create this Homepafe-Feature record.
        
        Returns:
            String containing initialization function for this record.
        """
        return '<HomepageFeatures(title=%r, body=%r, img_path_xs=%r, img_path_sm=%r, img_path_md=%r, img_path_lg=%r, is_active=%r)>' % (self.title, self.body, self.img_path_xs, self.img_path_sm, self.img_path_md, self.img_path_lg, self.is_active)


class HelpArticle(db.Model):
    """Set database model for Help Article."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    body = db.Column(db.Text, nullable=False)

    def __init__(
        self,
        title,
        description,
        body):
        """Creates a Help Article record.
        
        Args:
            title(str): Title of Help Article.
            description(str): Description text for Help Article.
            body(str): Body text for Help Article.
        """
        self.title = title
        self.description = description
        self.body = body

    @property
    def serialize(self):
        """Serializzes a Help Article record.
        
        Returns:
            Returns JSON dictionary of Help Article record."
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'body': self.body,
            }

    def __repr__(self):
        """Creates string representation of how to create this Help Article record.
        
        Returns:
            String containing initialization function for this record.
        """
        return '<HelpArticle(title=%r, description=%r, body=%r)>' % (self.title, self.description, self.body)
