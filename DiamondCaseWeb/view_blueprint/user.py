#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import validators
import email_validator

import hashlib

blueprint = Blueprint('user', __name__)
salt_val = 'salt'
hash_val = 'hash'
db = SQLAlchemy()

class LoginForm(Form):

    email = StringField('Email Address', [validators.Length(min=6,
                        max=60)])
    password = PasswordField('Password', [validators.DataRequired()])
    remember = BooleanField('Remember me')


class RegistrationForm(Form):

    email = StringField('Email Address', [validators.Length(min=6,
                        max=35)])
    password = PasswordField('New Password',
                             [validators.DataRequired(),
                             validators.EqualTo('confirm',
                             message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS',
                              [validators.DataRequired()])



#!/usr/bin/python
# -*- coding: utf-8 -*-


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = model.User.quert.filter(email=form.email).one()
        flask_login.login_user(user, remember=form.remember)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('authenication/login.html', form=form)


@blueprint.route('/signup')
def signup():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(name=form.username.data,
            phone=form.phone.data,
            username=form.username.data,
            email=form.email.data,
            salted_hashed_password=salt_and_hash(
                form.password.data
                )
            )
        db.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
#!/usr/bin/python
# -*- coding: utf-8 -*-


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(flask.url_for('index'))


@blueprint.route('/settings')
def settings():
    pass

@blueprint.route('/profile')
def profile():
    return render_template('profile.html', content='Profile Page',
                           twitter_conn=social.twitter.get_connection(),
                           facebook_conn=social.facebook.get_connection(),
                           foursquare_conn=social.foursquare.get_connection())