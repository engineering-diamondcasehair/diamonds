"""Blueprint for marketing pages."""
#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from jinja2 import TemplateNotFound
from DiamondCaseWeb.util.gen_util import getCategories

blueprint = Blueprint('marketing', __name__)
db = SQLAlchemy()

@blueprint.route('/campaign')
def campaign():
    """View Function for campaign pages.

    Returns:
        rendered template of view.
        """
    return render_template('campaign.html', 
        categories=getCategories())