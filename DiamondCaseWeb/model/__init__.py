#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from DiamondCaseWeb import create_app, db
from DiamondCaseWeb.model.product import  Product, ProductCategory, LocationProduct
from DiamondCaseWeb.model.static import HelpArticle, HomepageFeature
from DiamondCaseWeb.model.user import Role, User

if __name__ == "__main__":
	app = create_app()

	with app.app_context():
	    app.config.from_object('DiamondCaseWeb.config.TestingConfig')
	    db.init_app(app)
	    db.create_all()
	    db.session.commit()

	    app.config.from_object('DiamondCaseWeb.config.DevelopmentConfig')
	    db.init_app(app)
	    db.create_all()
	    db.session.commit()

else:
    __all__ = ['product', 'static', 'user']
    from . import product, static, user