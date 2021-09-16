# TODO: Write Test for Connections
from datetime import datetime
from DiamondCaseWeb import db
from DiamondCaseWeb.model.blog import BlogPostCategory, BlogPost
from DiamondCaseWeb.model import blog, product, static, user
from flask import Flask
from flask_testing import TestCase
import unittest


class ModelTests(TestCase):
    def setUp(self):
        self.app = self.create_app()
        self.context = self.app.app_context()
        self.context.push()
        self.db = db
        self.db.init_app(self.app)
        self.db.create_all()

    def tearDown(self):
        with self.app.app_context():
            self.db.drop_all()
            self.db.session.remove()
            self.db.session.expunge_all()
            self.db.session.close()
        self.context.pop()

    def create_app(self):
        app = Flask(__name__)
        app.config.from_object('DiamondCaseWeb.config.TestingConfig')
        return app

class ProductTest(ModelTests):
    def populate_product(self):
        self.category = product.ProductCategory(
            name='Category Name')
        self.db.session.add(self.category)
        self.db.session.commit()

        self.product = product.Product(
            name='name',
            short_description='short_description',
            long_description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eleifend tellus nec ultricies ultrices. Donec quis varius enim, quis vestibulum risus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas ut nisl tincidunt, imperdiet velit sit amet, dictum felis. Integer nisi nisl, tristique non velit ut, gravida hendrerit felis. Morbi ac auctor nunc, a malesuada massa. Morbi id eros vitae leo volutpat interdum. Nullam sodales ligula a nulla ultricies, a fermentum diam lacinia. In elit nisl, placerat at sapien ac, tristique tempus risus. Nunc tincidunt cursus semper. Sed sapien sapien, molestie eu diam eu, convallis tempus neque. Curabitur sed magna enim. Praesent porttitor nibh a eros sagittis malesuada. Nunc eget rhoncus dolor.',
            product_category_id=self.category.id,
            img_path_xs='path/to/img_path_xs',
            img_path_sm='path/to/img_path_sm',
            img_path_md='path/to/img_path_md',
            img_path_lg='path/to/img_path_lg')
        self.db.session.add(self.product)
        self.db.session.commit()


        self.location = product.Location(
            name='Location #1',
            description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eleifend tellus nec ultricies ultrices. Donec quis varius enim, quis vestibulum risus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas ut nisl tincidunt, imperdiet velit sit amet, dictum felis. Integer nisi nisl, tristique non velit ut, gravida hendrerit felis. Morbi ac auctor nunc, a malesuada massa. Morbi id eros vitae leo volutpat interdum. Nullam sodales ligula a nulla ultricies, a fermentum diam lacinia. In elit nisl, placerat at sapien ac, tristique tempus risus. Nunc tincidunt cursus semper. Sed sapien sapien, molestie eu diam eu, convallis tempus neque. Curabitur sed magna enim. Praesent porttitor nibh a eros sagittis malesuada. Nunc eget rhoncus dolor.',
            address1='213 Fake Street Blvd',
            address2='Ste. 213',
            city='Dallas',
            state='Texas',
            zip_code='12345',
            country='US',
            latitude=32.7767,
            longitude=-96.7970,
            direction_url='https://www.google.com/maps/dir/32.7257295,-96.8270816/Smokin%E2%80%99+Joe%E2%80%99s,+Dallas,+TX+75201/@32.7485566,-96.8433157,13z/data=!3m1!4b1!4m10!4m9!1m1!4e1!1m5!1m1!1s0x864e99b4794dab13:0x86f0f432c2333283!2m2!1d-96.7969879!2d32.7766642!3e0')
        self.db.session.add(self.location)
        self.db.session.commit()

        
        self.location_product = product.LocationProduct(
            location_id= self.location.id,
            product_id= self.product.id,
            price=12.23,
            num_available=10)
        self.db.session.add(self.location_product)
        self.db.session.commit()

    def test_category(self):
        with self.app.app_context():
            self.populate_product()
            expected = [self.category]
            expected_serial = {'id': 1, 'name': 'Category Name'}
            result = product.ProductCategory.query.all()
            result_serial = product.ProductCategory.query.first().serialize
            self.assertEqual(result, expected)
            self.assertEqual(result_serial, expected_serial)

    def test_product(self):
        with self.app.app_context():
            self.populate_product()
            expected = [self.product]
            expected_serial = {
                'id': 1, 
                'name': 'name', 
                'short_description': 'short_description', 
                'long_description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eleifend tellus nec ultricies ultrices. Donec quis varius enim, quis vestibulum risus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas ut nisl tincidunt, imperdiet velit sit amet, dictum felis. Integer nisi nisl, tristique non velit ut, gravida hendrerit felis. Morbi ac auctor nunc, a malesuada massa. Morbi id eros vitae leo volutpat interdum. Nullam sodales ligula a nulla ultricies, a fermentum diam lacinia. In elit nisl, placerat at sapien ac, tristique tempus risus. Nunc tincidunt cursus semper. Sed sapien sapien, molestie eu diam eu, convallis tempus neque. Curabitur sed magna enim. Praesent porttitor nibh a eros sagittis malesuada. Nunc eget rhoncus dolor.', 
                'product_category': {
                    'id': 1, 
                    'name': 'Category Name'
                }, 
                'images': {
                    'img_path_xs': 'path/to/img_path_xs', 
                    'img_path_sm': 'path/to/img_path_sm', 
                    'img_path_md': 'path/to/img_path_md', 
                    'img_path_lg': 'path/to/img_path_lg'
                }
            }
            result = product.Product.query.all()
            result_serial = product.Product.query.first().serialize
            self.assertEqual(result, expected)
            self.assertEqual(result_serial, expected_serial)


    def test_location(self):
        with self.app.app_context():
            self.populate_product()
            expected = [self.location]
            expected_serial = {
                'id': 1, 
                'name': 'Location #1', 
                'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eleifend tellus nec ultricies ultrices. Donec quis varius enim, quis vestibulum risus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas ut nisl tincidunt, imperdiet velit sit amet, dictum felis. Integer nisi nisl, tristique non velit ut, gravida hendrerit felis. Morbi ac auctor nunc, a malesuada massa. Morbi id eros vitae leo volutpat interdum. Nullam sodales ligula a nulla ultricies, a fermentum diam lacinia. In elit nisl, placerat at sapien ac, tristique tempus risus. Nunc tincidunt cursus semper. Sed sapien sapien, molestie eu diam eu, convallis tempus neque. Curabitur sed magna enim. Praesent porttitor nibh a eros sagittis malesuada. Nunc eget rhoncus dolor.', 
                'location': {
                    'address1': '213 Fake Street Blvd', 
                    'address2': 'Ste. 213', 
                    'city': 'Dallas', 
                    'state': 'Texas', 
                    'zip_code': '12345', 
                    'country': 'US', 
                    'coordinates': {
                        'latitude': 32.7767, 
                        'longitude': -96.797
                    }
                }, 
                'direction_url': 'https://www.google.com/maps/dir/32.7257295,-96.8270816/Smokin%E2%80%99+Joe%E2%80%99s,+Dallas,+TX+75201/@32.7485566,-96.8433157,13z/data=!3m1!4b1!4m10!4m9!1m1!4e1!1m5!1m1!1s0x864e99b4794dab13:0x86f0f432c2333283!2m2!1d-96.7969879!2d32.7766642!3e0'
            }
            result = product.Location.query.all()
            result_serial = product.Location.query.first().serialize
            self.assertEqual(result, expected)
            self.assertEqual(result_serial, expected_serial)

    def test_location_product(self):
        with self.app.app_context():
            self.populate_product()
            expected = [self.location_product]
            expected_serial = {
                'id': 1, 
                'location': {
                    'id': 1, 
                    'name': 'Location #1', 
                    'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eleifend tellus nec ultricies ultrices. Donec quis varius enim, quis vestibulum risus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas ut nisl tincidunt, imperdiet velit sit amet, dictum felis. Integer nisi nisl, tristique non velit ut, gravida hendrerit felis. Morbi ac auctor nunc, a malesuada massa. Morbi id eros vitae leo volutpat interdum. Nullam sodales ligula a nulla ultricies, a fermentum diam lacinia. In elit nisl, placerat at sapien ac, tristique tempus risus. Nunc tincidunt cursus semper. Sed sapien sapien, molestie eu diam eu, convallis tempus neque. Curabitur sed magna enim. Praesent porttitor nibh a eros sagittis malesuada. Nunc eget rhoncus dolor.', 
                    'location': {
                        'address1': '213 Fake Street Blvd', 
                        'address2': 'Ste. 213', 
                        'city': 'Dallas', 
                        'state': 'Texas', 
                        'zip_code': '12345', 
                        'country': 'US', 
                        'coordinates': {
                            'latitude': 32.7767, 
                            'longitude': -96.797
                        }
                    }, 
                    'direction_url': 'https://www.google.com/maps/dir/32.7257295,-96.8270816/Smokin%E2%80%99+Joe%E2%80%99s,+Dallas,+TX+75201/@32.7485566,-96.8433157,13z/data=!3m1!4b1!4m10!4m9!1m1!4e1!1m5!1m1!1s0x864e99b4794dab13:0x86f0f432c2333283!2m2!1d-96.7969879!2d32.7766642!3e0'
                }, 
                'product': {
                    'id': 1, 
                    'name': 'name', 
                    'short_description': 'short_description', 
                    'long_description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eleifend tellus nec ultricies ultrices. Donec quis varius enim, quis vestibulum risus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas ut nisl tincidunt, imperdiet velit sit amet, dictum felis. Integer nisi nisl, tristique non velit ut, gravida hendrerit felis. Morbi ac auctor nunc, a malesuada massa. Morbi id eros vitae leo volutpat interdum. Nullam sodales ligula a nulla ultricies, a fermentum diam lacinia. In elit nisl, placerat at sapien ac, tristique tempus risus. Nunc tincidunt cursus semper. Sed sapien sapien, molestie eu diam eu, convallis tempus neque. Curabitur sed magna enim. Praesent porttitor nibh a eros sagittis malesuada. Nunc eget rhoncus dolor.', 
                    'product_category': {
                        'id': 1, 
                        'name': 'Category Name'
                    }, 
                    'images': {
                        'img_path_xs': 'path/to/img_path_xs', 
                        'img_path_sm': 'path/to/img_path_sm', 
                        'img_path_md': 'path/to/img_path_md', 
                        'img_path_lg': 'path/to/img_path_lg'
                    }
                }, 
                'price': 12.23, 
                'num_available': 10
            }
            result = product.LocationProduct.query.all()
            result_serial = product.LocationProduct.query.first().serialize
            self.assertEqual(result, expected)        
            self.assertEqual(result_serial, expected_serial)



class StaticTest(ModelTests):
    def populate_static(self):
        self.homepage_feature = static.HomepageFeature(
            title='Feature Title',
            body='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eleifend tellus nec ultricies ultrices. Donec quis varius enim, quis vestibulum risus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas ut nisl tincidunt, imperdiet velit sit amet, dictum felis. Integer nisi nisl, tristique non velit ut, gravida hendrerit felis. Morbi ac auctor nunc, a malesuada massa. Morbi id eros vitae leo volutpat interdum. Nullam sodales ligula a nulla ultricies, a fermentum diam lacinia. In elit nisl, placerat at sapien ac, tristique tempus risus. Nunc tincidunt cursus semper. Sed sapien sapien, molestie eu diam eu, convallis tempus neque. Curabitur sed magna enim. Praesent porttitor nibh a eros sagittis malesuada. Nunc eget rhoncus dolor.',
            img_path_xs='path/to/img_path_xs',
            img_path_sm='path/to/img_path_sm',
            img_path_md='path/to/img_path_md',
            img_path_lg='path/to/img_path_lg',
            is_active=True)
        db.session.add(self.homepage_feature)
        db.session.commit()

        self.help_aticle = static.HelpArticle(
            title='Title',
            description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eleifend tellus nec ultricies ultrices.',
            body='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eleifend tellus nec ultricies ultrices. Donec quis varius enim, quis vestibulum risus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas ut nisl tincidunt, imperdiet velit sit amet, dictum felis. Integer nisi nisl, tristique non velit ut, gravida hendrerit felis. Morbi ac auctor nunc, a malesuada massa. Morbi id eros vitae leo volutpat interdum. Nullam sodales ligula a nulla ultricies, a fermentum diam lacinia. In elit nisl, placerat at sapien ac, tristique tempus risus. Nunc tincidunt cursus semper. Sed sapien sapien, molestie eu diam eu, convallis tempus neque. Curabitur sed magna enim. Praesent porttitor nibh a eros sagittis malesuada. Nunc eget rhoncus dolor.')
        db.session.add(self.help_aticle)
        db.session.commit()

    # def setUp(self):
    #     super().setUp()

    def test_homepage_feature(self):
        with self.app.app_context():
            self.populate_static()
            expected = [self.homepage_feature]
            expected_serial = {
                'id': 1, 
                'title': 'Feature Title', 
                'body': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eleifend tellus nec ultricies ultrices. Donec quis varius enim, quis vestibulum risus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas ut nisl tincidunt, imperdiet velit sit amet, dictum felis. Integer nisi nisl, tristique non velit ut, gravida hendrerit felis. Morbi ac auctor nunc, a malesuada massa. Morbi id eros vitae leo volutpat interdum. Nullam sodales ligula a nulla ultricies, a fermentum diam lacinia. In elit nisl, placerat at sapien ac, tristique tempus risus. Nunc tincidunt cursus semper. Sed sapien sapien, molestie eu diam eu, convallis tempus neque. Curabitur sed magna enim. Praesent porttitor nibh a eros sagittis malesuada. Nunc eget rhoncus dolor.', 
                'images': {
                    'img_path_xs': 'path/to/img_path_xs', 
                    'img_path_sm': 'path/to/img_path_sm', 
                    'img_path_md': 'path/to/img_path_md', 
                    'img_path_lg': 'path/to/img_path_lg'
                }, 
                'is_active': True
            }
            
            result = static.HomepageFeature.query.all()
            result_serial = static.HomepageFeature.query.first().serialize
            
            self.assertEqual(result, expected)  
            self.assertEqual(result_serial, expected_serial)  

    def test_help_aticle(self):
        with self.app.app_context():
            self.populate_static()
            expected = [self.help_aticle]
            expected_serial = {
                'id': 1, 
                'title': 'Title', 
                'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eleifend tellus nec ultricies ultrices.', 'body': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eleifend tellus nec ultricies ultrices. Donec quis varius enim, quis vestibulum risus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Maecenas ut nisl tincidunt, imperdiet velit sit amet, dictum felis. Integer nisi nisl, tristique non velit ut, gravida hendrerit felis. Morbi ac auctor nunc, a malesuada massa. Morbi id eros vitae leo volutpat interdum. Nullam sodales ligula a nulla ultricies, a fermentum diam lacinia. In elit nisl, placerat at sapien ac, tristique tempus risus. Nunc tincidunt cursus semper. Sed sapien sapien, molestie eu diam eu, convallis tempus neque. Curabitur sed magna enim. Praesent porttitor nibh a eros sagittis malesuada. Nunc eget rhoncus dolor.'
            }

            result = static.HelpArticle.query.all()
            result_serial = static.HelpArticle.query.first().serialize
            
            self.assertEqual(result, expected)        
            self.assertEqual(result_serial, expected_serial)        


class UserTest(ModelTests):

    def populate_user(self):
        self.role = user.Role(
            name='admin',
            description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eleifend tellus nec ultricies ultrices.')
        db.session.add(self.role)
        db.session.commit()

        self.user = user.User(
            name='John Doe',
            phone='2145551234',
            email='fake_account@example.com',
            password='PASSWORD123!',
            confirmed_at=datetime(2021, 8, 9, 3, 23, 30, 817086),
            role_id=self.role.id)
        db.session.add(self.user)
        db.session.commit()

    # def setUp(self):
    #     super().setUp()
        

    def test_role(self):
        with self.app.app_context():
            self.populate_user()
            expected = [self.role]
            expected_serial = {
                'id': 1, 
                'name': 'admin', 
                'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eleifend tellus nec ultricies ultrices.'
            }
            result = user.Role.query.all()
            result_serial = user.Role.query.first().serialize
            
            self.assertEqual(result, expected)  
            self.assertEqual(result_serial, expected_serial)  

    def test_users(self):
        with self.app.app_context():
            self.populate_user()
            expected = [self.user]
            expected_serial = {
                'id': 1, 
                'name': 'John Doe', 
                'phone': '2145551234', 
                'email': 'fake_account@example.com', 
                'active': False, 
                'banned': False, 
                'confirmed_at': datetime(2021, 8, 9, 3, 23, 30, 817086).isoformat(), 
                'role': {
                    'id': 1, 
                    'name': 'admin', 
                    'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam eleifend tellus nec ultricies ultrices.'
                }
            }
            result = user.User.query.all()
            result_serial = user.User.query.first().serialize
            
            self.assertEqual(result, expected)        
            self.assertEqual(result_serial['id'], expected_serial['id'])
            self.assertEqual(result_serial['name'], expected_serial['name'])
            self.assertEqual(result_serial['phone'], expected_serial['phone'])
            self.assertEqual(result_serial['email'], expected_serial['email'])
            self.assertEqual(result_serial['active'], expected_serial['active'])
            self.assertEqual(result_serial['banned'], expected_serial['banned'])
            self.assertEqual(result_serial['confirmed_at'], expected_serial['confirmed_at'])
            self.assertEqual(result_serial['role']['id'], expected_serial['role']['id'])
            self.assertEqual(result_serial['role']['name'], expected_serial['role']['name'])
            self.assertEqual(result_serial['role']['description'], expected_serial['role']['description'])

if __name__ == '__main__':
    unittest.main()