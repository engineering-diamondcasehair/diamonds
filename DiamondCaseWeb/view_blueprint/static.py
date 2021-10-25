"""Blueprint for static pages."""
#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort, request
from flask_sqlalchemy import SQLAlchemy
from jinja2 import TemplateNotFound
from wtforms import Form, BooleanField, StringField, TextAreaField, \
    validators
from DiamondCaseWeb.model.static import HelpArticle, HomepageFeature
from DiamondCaseWeb.util.gen_util import getCategories


blueprint = Blueprint('static', __name__)
db = SQLAlchemy()

class ContactForm(Form):
    """WTForm implementation of contact form."""
    name = StringField('Name', [validators.Length(min=2, max=25)])
    email = StringField('Email Address', [validators.Length(min=6,
                        max=60)])
    subject = StringField('Subject', [validators.Length(min=6, max=30)])
    message = TextAreaField('Message')


@blueprint.route('/')
@blueprint.route('/index')
def index():
    """View Function for home page.

    Returns:
        rendered template of view
    """
    # TODO: Change data model

    features = HomepageFeature.query.filter_by(is_active=True).all()
    return render_template('homepage.html', features=features, categories=getCategories())


@blueprint.route('/about')
def about():
    """View Function for about page.

    Returns:
        rendered template of view
    """
    return render_template('about.html', categories=getCategories())


@blueprint.route('/help')
def help():
    """View Function for help page.

    Returns:
        rendered template of view
    """
    help_articles = HelpArticle.query.all()
    return render_template('help.html', 
        help_articles=help_articles, 
        categories=getCategories())


@blueprint.route('/terms')
def terms():
    """View Function for term of service page.

    Returns:
        rendered template of view
    """
    return render_template('terms.html', categories=getCategories())


@blueprint.route('/contact', methods=['GET', 'POST'])
def contact():
    """View Function for contact page.

    Returns:
        rendered template of view
    """
    form = ContactForm(request.form)
    if request.method == 'POST' and form.validate():
        dc_mail.send_message(sender=(form.name.data, form.email.data),
                             subject=form.subject.data,
                             message=form.message.data, app=app,
                             mail=mail)
        flash('Thanks for your message')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form, categories=getCategories())
