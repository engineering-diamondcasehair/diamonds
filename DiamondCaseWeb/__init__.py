"""Main file for Web app creation."""
from DiamondCaseWeb.util import assets
from DiamondCaseWeb.util import dc_mail
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

# Main SQL Alchemy database object
db = SQLAlchemy()

def create_app():
    """Initializes, configures and returns Flask App Instance object."""

    # create and configure the app
    app = Flask(__name__)
    app.config.from_object('DiamondCaseWeb.config.DevelopmentConfig')

    # Register SCSS assets
    assets.register_assets(app)

    # Set up mail
    mail = dc_mail.setup_mail(app)

    # Setup Database
    from DiamondCaseWeb.model.product import  Product, ProductCategory, LocationProduct
    from DiamondCaseWeb.model.static import HelpArticle, HomepageFeature
    from DiamondCaseWeb.model.user import Role, User
    db.init_app(app)


    from DiamondCaseWeb.view_blueprint import marketing as marketing_bp
    from DiamondCaseWeb.view_blueprint import product as product_bp
    from DiamondCaseWeb.view_blueprint import shop as shop_bp
    from DiamondCaseWeb.view_blueprint import static as static_bp
    from DiamondCaseWeb.view_blueprint import user as user_bp

    # Register view blueprints
    app.register_blueprint(marketing_bp.blueprint)
    app.register_blueprint(product_bp.blueprint)
    app.register_blueprint(shop_bp.blueprint)
    app.register_blueprint(static_bp.blueprint)
    app.register_blueprint(user_bp.blueprint)


    from DiamondCaseWeb.api import help_article as help_article_api_bp
    from DiamondCaseWeb.api import homepage_feature as homepage_feature_api_bp
    from DiamondCaseWeb.api import location as location_api_bp
    from DiamondCaseWeb.api import location_product as location_product_api_bp
    from DiamondCaseWeb.api import product as product_api_bp
    from DiamondCaseWeb.api import product_category as product_category_api_bp
    from DiamondCaseWeb.api import role as role_api_bp
    from DiamondCaseWeb.api import user as user_api_bp

    # Register api blueprints
    app.register_blueprint(help_article_api_bp.blueprint)
    app.register_blueprint(homepage_feature_api_bp.blueprint)
    app.register_blueprint(location_api_bp.blueprint)
    app.register_blueprint(location_product_api_bp.blueprint)
    app.register_blueprint(product_api_bp.blueprint)
    app.register_blueprint(product_category_api_bp.blueprint)
    app.register_blueprint(role_api_bp.blueprint)
    app.register_blueprint(user_api_bp.blueprint)

    # Admin Dashboard
    @app.route('/admin')
    def admin_backend():
        return app.send_static_file("back_office/index.html")


    return app

from DiamondCaseWeb import config