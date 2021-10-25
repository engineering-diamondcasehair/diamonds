"""Utility file to seed tracker database from data in seed_data/"""

from DiamondCaseWeb.model.product import ProductCategory as ProductCategoryModel
from DiamondCaseWeb.model.product import Product as ProductModel
from DiamondCaseWeb.model.product import Location as LocationModel
from DiamondCaseWeb.model.product import LocationProduct as LocationProductModel
from DiamondCaseWeb.model.static import HomepageFeature as HomepageFeatureModel
from DiamondCaseWeb.model.static import HelpArticle as HelpArticleModel
from DiamondCaseWeb.model.user import Role as RoleModel
from DiamondCaseWeb.model.user import User as UserModel 
# from DiamondCaseWeb.model.user import Order as OrderModel 
from DiamondCaseWeb import create_app, db


def load_products():
    """Load users from u.user into database."""

    for i, row in enumerate(open("seed_data/category.product")):
        row = row.rstrip()
        name = row.split("|")
        product_category = ProductCategoryModel(name=name)
        db.session.add(product_category)

    for i, row in enumerate(open("seed_data/product.product")):
        row = row.rstrip()
        name, short_description, long_description, product_category_id, img_path_xs, img_path_sm, img_path_md, img_path_lg = row.split("|")
        product = ProductModel(name=name,
            short_description=short_description,
            long_description=long_description,
            product_category_id=product_category_id,
            img_path_xs=img_path_xs,
            img_path_sm=img_path_sm,
            img_path_md=img_path_md,
            img_path_lg=img_path_lg)
        db.session.add(product)

    for i, row in enumerate(open("seed_data/location.product")):
        row = row.rstrip()
        name, description, address1, address2, city, state, zip_code, country, latitude, longitude, direction_url = row.split("|")
        location = LocationModel(name=name,
            description=description,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country,
            latitude=latitude,
            longitude=longitude,
            direction_url=direction_url)
        db.session.add(location)

    for i, row in enumerate(open("seed_data/location_product.product")):
        row = row.rstrip()
        location_id, product_id, price, num_available = row.split("|")
        location_product = LocationProductModel(location_id=location_id,
            product_id=product_id,
            price=price,
            num_available=num_available)
        db.session.add(location_product)

    db.session.commit()


def load_static():
    """Load users from u.user into database."""

    for i, row in enumerate(open("seed_data/homepage_feature.static")):
        row = row.rstrip()
        title, body, img_path_xs, img_path_sm, img_path_md, img_path_lg, is_active = row.split("|")
        homepage_feature = HomepageFeatureModel(title=title,
            body=body,
            img_path_xs=img_path_xs,
            img_path_sm=img_path_sm,
            img_path_md=img_path_md,
            img_path_lg=img_path_lg,
            is_active=is_active)
        db.session.add(homepage_feature)

    for i, row in enumerate(open("seed_data/help_article.static")):
        row = row.rstrip()
        title, description, body = row.split("|")
        help_article = HelpArticleModel(title=title, 
            description=description, 
            body=body)
        db.session.add(help_article)

    db.session.commit()


def load_user():
    """Load users from u.user into database."""

    for i, row in enumerate(open("seed_data/role.user")):
        row = row.rstrip()
        name, description = row.split("|")
        role = RoleModel(name=name, description=description)
        db.session.add(role)

    for i, row in enumerate(open("seed_data/user.user")):
        row = row.rstrip()
        name, phone, email, password, confirmed_at, role_id = row.split("|")
        user = UserModel(name=name,
            phone=phone,
            email=email,
            password=password,
            confirmed_at=confirmed_at,
            role_id=role_id)
        db.session.add(user)

    # for i, row in enumerate(open("seed_data/order.user")):
    #     row = row.rstrip()
    #     active, user_id, product_location_id = row.split("|")
    #     order = OrderrModel(
    #         active=active, 
    #         user_id=user_id, 
    #         product_location_id=product_location_id)
    #     db.session.add(order)

    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    app.config.from_object('DiamondCaseWeb.config.DevelopmentConfig')
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()

    load_products()
    load_static()
    load_user()