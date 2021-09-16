import datetime
from DiamondCaseWeb import create_app, db
from DiamondCaseWeb.model.blog import BlogPostCategory as BlogPostCategoryModel
from DiamondCaseWeb.model.blog import BlogPost as BlogPostModel
from DiamondCaseWeb.model.static import HomepageFeature as HomepageFeatureModel
from DiamondCaseWeb.model.static import HelpArticle as HelpArticleModel
from DiamondCaseWeb.model.product import ProductCategory as ProductCategoryModel
from DiamondCaseWeb.model.product import Product as ProductModel
from DiamondCaseWeb.model.product import Location as LocationModel
from DiamondCaseWeb.model.product import LocationProduct as LocationProductModel
from DiamondCaseWeb.model.user import Role as RoleModel
from DiamondCaseWeb.model.user import User as UserModel
from flask import Flask
import json
import unittest

class ApiTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.context = self.app.app_context()
        self.app.config.from_object('DiamondCaseWeb.config.TestingConfig')
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

    def client_open(self, url, method, data={}):
        with self.app.app_context():
            with self.app.test_client() as client:
                result = client.open(url, method=method, json=data)
        return result

class HomepageFeatureTest(ApiTests):
    def test_post(self):
        payload = {
            'title': 'title',
            'body': 'body',
            'img_path_xs': 'path/to/img_path_xs',
            'img_path_sm': 'path/to/img_path_sm',
            'img_path_md': 'path/to/img_path_md',
            'img_path_lg': 'path/to/img_path_lg',
            'is_active': True
        }

        response = self.client_open(
            '/api/homepage_features', 
            'POST', 
            data=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.json), 5)
        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(str, type(response.json['title']))
        self.assertEqual(str, type(response.json['body']))
        self.assertEqual(str, type(response.json['images']['img_path_xs']))
        self.assertEqual(str, type(response.json['images']['img_path_sm']))
        self.assertEqual(str, type(response.json['images']['img_path_md']))
        self.assertEqual(str, type(response.json['images']['img_path_lg']))
        self.assertEqual(bool, type(response.json['is_active']))

        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['title'], 'title')
        self.assertEqual(response.json['body'], 'body')
        self.assertEqual(response.json['images']['img_path_xs'], 'path/to/img_path_xs')
        self.assertEqual(response.json['images']['img_path_sm'], 'path/to/img_path_sm')
        self.assertEqual(response.json['images']['img_path_md'], 'path/to/img_path_md')
        self.assertEqual(response.json['images']['img_path_lg'], 'path/to/img_path_lg')
        self.assertEqual(response.json['is_active'], True)

    def test_get_all(self):
        home_feature  = HomepageFeatureModel(
            title='title',
            body='body',
            img_path_xs='path/to/img_path_xs',
            img_path_sm='path/to/img_path_sm',
            img_path_md='path/to/img_path_md',
            img_path_lg='path/to/img_path_lg',
            is_active=True)
        self.db.session.add(home_feature)
        self.db.session.commit()

        response = self.client_open(
            '/api/homepage_features', 
            'GET')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list, type(response.json))

        self.assertEqual(len(response.json), 1)
        self.assertEqual(int, type(response.json[0]['id']))
        self.assertEqual(str, type(response.json[0]['title']))
        self.assertEqual(str, type(response.json[0]['body']))
        self.assertEqual(str, type(response.json[0]['images']['img_path_xs']))
        self.assertEqual(str, type(response.json[0]['images']['img_path_sm']))
        self.assertEqual(str, type(response.json[0]['images']['img_path_md']))
        self.assertEqual(str, type(response.json[0]['images']['img_path_lg']))
        self.assertEqual(bool, type(response.json[0]['is_active']))

        self.assertEqual(response.json[0]['id'], 1)
        self.assertEqual(response.json[0]['title'], 'title')
        self.assertEqual(response.json[0]['body'], 'body')
        self.assertEqual(response.json[0]['images']['img_path_xs'], 'path/to/img_path_xs')
        self.assertEqual(response.json[0]['images']['img_path_sm'], 'path/to/img_path_sm')
        self.assertEqual(response.json[0]['images']['img_path_md'], 'path/to/img_path_md')
        self.assertEqual(response.json[0]['images']['img_path_lg'], 'path/to/img_path_lg')
        self.assertEqual(response.json[0]['is_active'], True)

    def test_get_one(self):
        home_feature  = HomepageFeatureModel(
            title='title',
            body='body',
            img_path_xs='path/to/img_path_xs',
            img_path_sm='path/to/img_path_sm',
            img_path_md='path/to/img_path_md',
            img_path_lg='path/to/img_path_lg',
            is_active=True)
        self.db.session.add(home_feature)
        self.db.session.commit()

        response = self.client_open(
            '/api/homepage_feature/1', 
            'GET')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(dict, type(response.json))
        self.assertEqual(len(response.json), 5)
        
        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(str, type(response.json['title']))
        self.assertEqual(str, type(response.json['body']))
        self.assertEqual(str, type(response.json['images']['img_path_xs']))
        self.assertEqual(str, type(response.json['images']['img_path_sm']))
        self.assertEqual(str, type(response.json['images']['img_path_md']))
        self.assertEqual(str, type(response.json['images']['img_path_lg']))
        self.assertEqual(bool, type(response.json['is_active']))

        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['title'], 'title')
        self.assertEqual(response.json['body'], 'body')
        self.assertEqual(response.json['images']['img_path_xs'], 'path/to/img_path_xs')
        self.assertEqual(response.json['images']['img_path_sm'], 'path/to/img_path_sm')
        self.assertEqual(response.json['images']['img_path_md'], 'path/to/img_path_md')
        self.assertEqual(response.json['images']['img_path_lg'], 'path/to/img_path_lg')
        self.assertEqual(response.json['is_active'], True)

    def test_put_one(self):
        home_feature  = HomepageFeatureModel(
            title='title',
            body='body',
            img_path_xs='path/to/img_path_xs',
            img_path_sm='path/to/img_path_sm',
            img_path_md='path/to/img_path_md',
            img_path_lg='path/to/img_path_lg',
            is_active=True)
        self.db.session.add(home_feature)
        self.db.session.commit()

        response = self.client_open(
            '/api/homepage_feature/1', 
            'PUT',
            {
                'title': 'changed title',
                'body': 'changed body',
                'img_path_xs': 'path/to/img_path_xs',
                'img_path_sm': 'path/to/img_path_sm',
                'img_path_md': 'path/to/img_path_md',
                'img_path_lg': 'path/to/img_path_lg',
                'is_active': True
            })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(dict, type(response.json))
        self.assertEqual(len(response.json), 5)

        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(str, type(response.json['title']))
        self.assertEqual(str, type(response.json['body']))
        self.assertEqual(len(response.json['images']), 4)
        self.assertEqual(str, type(response.json['images']['img_path_xs']))
        self.assertEqual(str, type(response.json['images']['img_path_sm']))
        self.assertEqual(str, type(response.json['images']['img_path_md']))
        self.assertEqual(str, type(response.json['images']['img_path_lg']))
        self.assertEqual(bool, type(response.json['is_active']))

        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['title'], 'changed title')
        self.assertEqual(response.json['body'], 'changed body')
        self.assertEqual(response.json['images']['img_path_xs'], 'path/to/img_path_xs')
        self.assertEqual(response.json['images']['img_path_sm'], 'path/to/img_path_sm')
        self.assertEqual(response.json['images']['img_path_md'], 'path/to/img_path_md')
        self.assertEqual(response.json['images']['img_path_lg'], 'path/to/img_path_lg')
        self.assertEqual(response.json['is_active'], True)

    def test_delete_one(self):
        home_feature  = HomepageFeatureModel(
            title='title',
            body='body',
            img_path_xs='path/to/img_path_xs',
            img_path_sm='path/to/img_path_sm',
            img_path_md='path/to/img_path_md',
            img_path_lg='path/to/img_path_lg',
            is_active=True)
        self.db.session.add(home_feature)
        self.db.session.commit()

        response = self.client_open(
            '/api/homepage_feature/1', 
            'DELETE')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(HomepageFeatureModel.query.all()), 0)


class HelpArticleTest(ApiTests):
    def test_post(self):
        payload = {
            'title': 'Title',
            'description': 'Description',
            'body': 'Body'
        }

        response = self.client_open(
            '/api/help_articles', 
            'POST', 
            data=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.json), 4)
        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(str, type(response.json['title']))
        self.assertEqual(str, type(response.json['description']))
        self.assertEqual(str, type(response.json['body']))

        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['title'], 'Title')
        self.assertEqual(response.json['description'], 'Description')
        self.assertEqual(response.json['body'], 'Body')

    def test_get_all(self):
        help_article  = HelpArticleModel(
            title='Title',
            description='Description',
            body='Body')
        self.db.session.add(help_article)
        self.db.session.commit()

        response = self.client_open(
            '/api/help_articles', 
            'GET')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list, type(response.json))

        self.assertEqual(len(response.json), 1)
        self.assertEqual(list, type(response.json))
        self.assertEqual(dict, type(response.json[0]))
        self.assertEqual(int, type(response.json[0]['id']))
        self.assertEqual(str, type(response.json[0]['title']))
        self.assertEqual(str, type(response.json[0]['body']))
        self.assertEqual(str, type(response.json[0]['description']))

        self.assertEqual(response.json[0]['id'], 1)
        self.assertEqual(response.json[0]['title'], 'Title')
        self.assertEqual(response.json[0]['body'], 'Body')
        self.assertEqual(response.json[0]['description'], 'Description')

    def test_get_one(self):
        home_feature  = HelpArticleModel(
            title='Title',
            description='Description',
            body='Body')
        self.db.session.add(home_feature)
        self.db.session.commit()

        response = self.client_open(
            '/api/help_article/1', 
            'GET')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(dict, type(response.json))
        self.assertEqual(len(response.json), 4)
        
        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(str, type(response.json['title']))
        self.assertEqual(str, type(response.json['description']))
        self.assertEqual(str, type(response.json['body']))

        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['title'], 'Title')
        self.assertEqual(response.json['description'], 'Description')
        self.assertEqual(response.json['body'], 'Body')

    def test_put_one(self):
        help_article  = HelpArticleModel(
            title='Title',
            description='Description',
            body='Body')
        self.db.session.add(help_article)
        self.db.session.commit()

        response = self.client_open(
            '/api/help_article/1', 
            'PUT',
            {
                'title': 'changed title',
                'description': 'changed description',
                'body': 'changed body'
            })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(dict, type(response.json))
        self.assertEqual(len(response.json), 4)

        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(str, type(response.json['title']))
        self.assertEqual(str, type(response.json['description']))
        self.assertEqual(str, type(response.json['body']))

        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['title'], 'changed title')
        self.assertEqual(response.json['description'], 'changed description')
        self.assertEqual(response.json['body'], 'changed body')

    def test_delete_one(self):
        help_article  = HelpArticleModel(
            title='Title',
            description='Description',
            body='Body')
        self.db.session.add(help_article)
        self.db.session.commit()

        response = self.client_open(
            '/api/help_article/1', 
            'DELETE')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(HelpArticleModel.query.all()), 0)


class LocationTest(ApiTests):
    def test_post(self):
        payload = {
            'name': 'Location 1',
            'description': 'Description 1',
            'address1': '123 Fake St.',
            'address2': '#1234',
            'city': 'Dallas',
            'state': 'Texas',
            'zip_code': 12345,
            'country': 'United State of America',
            'latitude': 123.345,
            'longitude': 123.345,
            'direction_url': 'https://maps.com/direction/to/location'
        }

        response = self.client_open(
            '/api/locations', 
            'POST', 
            data=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.json), 5)
        self.assertEqual(len(response.json['location']), 7)
        self.assertEqual(len(response.json['location']['coordinates']), 2)

        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(str, type(response.json['name']))
        self.assertEqual(str, type(response.json['description']))
        self.assertEqual(str, type(response.json['location']['address1']))
        self.assertEqual(str, type(response.json['location']['address2']))
        self.assertEqual(str, type(response.json['location']['city']))
        self.assertEqual(str, type(response.json['location']['state']))
        self.assertEqual(str, type(response.json['location']['state']))
        self.assertEqual(str, type(response.json['location']['country']))
        self.assertEqual(float, type(response.json['location']['coordinates']['latitude']))
        self.assertEqual(float, type(response.json['location']['coordinates']['longitude']))
        self.assertEqual(str, type(response.json['direction_url']))

        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['name'], 'Location 1')
        self.assertEqual(response.json['description'], 'Description 1')
        self.assertEqual(response.json['location']['address1'], '123 Fake St.')
        self.assertEqual(response.json['location']['address2'], '#1234')
        self.assertEqual(response.json['location']['city'], 'Dallas')
        self.assertEqual(response.json['location']['state'], 'Texas')
        self.assertEqual(response.json['location']['zip_code'], '12345')
        self.assertEqual(response.json['location']['country'], 'United State of America')
        self.assertEqual(response.json['location']['coordinates']['latitude'], 123.345)
        self.assertEqual(response.json['location']['coordinates']['longitude'], 123.345)
        self.assertEqual(response.json['direction_url'], 'https://maps.com/direction/to/location')

    def test_get_all(self):
        location  = LocationModel(
            name='Location 1',
            description='Description 1',
            address1='123 Fake St.',
            address2='#1234',
            city='Dallas',
            state='Texas',
            zip_code=12345,
            country='United States of America',
            latitude=123.345,
            longitude=123.345,
            direction_url='https://maps.com/direction/to/location')
        self.db.session.add(location)
        self.db.session.commit()

        response = self.client_open(
            '/api/locations', 
            'GET')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list, type(response.json))

        self.assertEqual(len(response.json), 1)
        self.assertEqual(list, type(response.json))
        self.assertEqual(dict, type(response.json[0]))
        self.assertEqual(int, type(response.json[0]['id']))
        self.assertEqual(str, type(response.json[0]['name']))
        self.assertEqual(str, type(response.json[0]['description']))
        self.assertEqual(dict, type(response.json[0]['location']))
        self.assertEqual(str, type(response.json[0]['location']['address1']))
        self.assertEqual(str, type(response.json[0]['location']['address2']))
        self.assertEqual(str, type(response.json[0]['location']['city']))
        self.assertEqual(str, type(response.json[0]['location']['zip_code']))
        self.assertEqual(str, type(response.json[0]['location']['state']))
        self.assertEqual(str, type(response.json[0]['location']['country']))
        self.assertEqual(dict, type(response.json[0]['location']['coordinates']))
        self.assertEqual(float, type(response.json[0]['location']['coordinates']['latitude']))
        self.assertEqual(float, type(response.json[0]['location']['coordinates']['longitude']))
        self.assertEqual(str, type(response.json[0]['direction_url']))

        self.assertEqual(response.json[0]['id'], 1)
        self.assertEqual(response.json[0]['name'], 'Location 1')
        self.assertEqual(response.json[0]['description'], 'Description 1')
        self.assertEqual(response.json[0]['location']['address1'], '123 Fake St.')
        self.assertEqual(response.json[0]['location']['address2'], '#1234')
        self.assertEqual(response.json[0]['location']['city'], 'Dallas')
        self.assertEqual(response.json[0]['location']['zip_code'], '12345')
        self.assertEqual(response.json[0]['location']['state'], 'Texas')
        self.assertEqual(response.json[0]['location']['country'], 'United States of America')
        self.assertEqual(response.json[0]['location']['coordinates']['latitude'], 123.345)
        self.assertEqual(response.json[0]['location']['coordinates']['longitude'], 123.345)
        self.assertEqual(response.json[0]['direction_url'], 'https://maps.com/direction/to/location')

    def test_get_one(self):
        location  = LocationModel(
            name='Location 1',
            description='Description 1',
            address1='123 Fake St.',
            address2='#1234',
            city='Dallas',
            state='Texas',
            zip_code=12345,
            country='United States of America',
            latitude=123.345,
            longitude=123.345,
            direction_url='https://maps.com/direction/to/location')
        self.db.session.add(location)
        self.db.session.commit()

        response = self.client_open(
            '/api/location/1', 
            'GET')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(dict, type(response.json))
        self.assertEqual(len(response.json), 5)
        
        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(str, type(response.json['name']))
        self.assertEqual(str, type(response.json['description']))
        self.assertEqual(str, type(response.json['location']['address1']))
        self.assertEqual(str, type(response.json['location']['address2']))
        self.assertEqual(str, type(response.json['location']['city']))
        self.assertEqual(str, type(response.json['location']['state']))
        self.assertEqual(str, type(response.json['location']['state']))
        self.assertEqual(str, type(response.json['location']['country']))
        self.assertEqual(float, type(response.json['location']['coordinates']['latitude']))
        self.assertEqual(float, type(response.json['location']['coordinates']['longitude']))
        self.assertEqual(str, type(response.json['direction_url']))

        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['name'], 'Location 1')
        self.assertEqual(response.json['description'], 'Description 1')
        self.assertEqual(response.json['location']['address1'], '123 Fake St.')
        self.assertEqual(response.json['location']['address2'], '#1234')
        self.assertEqual(response.json['location']['city'], 'Dallas')
        self.assertEqual(response.json['location']['state'], 'Texas')
        self.assertEqual(response.json['location']['zip_code'], '12345')
        self.assertEqual(response.json['location']['country'], 'United States of America')
        self.assertEqual(response.json['location']['coordinates']['latitude'], 123.345)
        self.assertEqual(response.json['location']['coordinates']['longitude'], 123.345)
        self.assertEqual(response.json['direction_url'], 'https://maps.com/direction/to/location')

    def test_put_one(self):
        location  = LocationModel(
            name='Location 1',
            description='Description 1',
            address1='123 Fake St.',
            address2='#1234',
            city='Dallas',
            state='Texas',
            zip_code=12345,
            country='United States of America',
            latitude=123.345,
            longitude=123.345,
            direction_url='https://maps.com/direction/to/location')
        self.db.session.add(location)
        self.db.session.commit()

        response = self.client_open(
            '/api/location/1', 
            'PUT',
            {
                'name': 'Location 2',
                'description': 'Description 2',
                'address1': '123 Real St.',
                'address2': '#5678',
                'city': 'Fort Worth',
                'state': 'Texas',
                'zip_code': 67890,
                'country': 'United State of America',
                'latitude': 123.456,
                'longitude': 123.456,
                'direction_url': 'https://maps.com/direction/to/location2'
            })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(dict, type(response.json))
        self.assertEqual(len(response.json), 5)

        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(str, type(response.json['name']))
        self.assertEqual(str, type(response.json['description']))
        self.assertEqual(str, type(response.json['location']['address1']))
        self.assertEqual(str, type(response.json['location']['address2']))
        self.assertEqual(str, type(response.json['location']['city']))
        self.assertEqual(str, type(response.json['location']['state']))
        self.assertEqual(str, type(response.json['location']['state']))
        self.assertEqual(str, type(response.json['location']['country']))
        self.assertEqual(float, type(response.json['location']['coordinates']['latitude']))
        self.assertEqual(float, type(response.json['location']['coordinates']['longitude']))
        self.assertEqual(str, type(response.json['direction_url']))

        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['name'], 'Location 2')
        self.assertEqual(response.json['description'], 'Description 2')
        self.assertEqual(response.json['location']['address1'], '123 Real St.')
        self.assertEqual(response.json['location']['address2'], '#5678')
        self.assertEqual(response.json['location']['city'], 'Fort Worth')
        self.assertEqual(response.json['location']['state'], 'Texas')
        self.assertEqual(response.json['location']['zip_code'], '67890')
        self.assertEqual(response.json['location']['country'], 'United State of America')
        self.assertEqual(response.json['location']['coordinates']['latitude'], 123.456)
        self.assertEqual(response.json['location']['coordinates']['longitude'], 123.456)
        self.assertEqual(response.json['direction_url'], 'https://maps.com/direction/to/location2')

    def test_delete_one(self):
        location  = LocationModel(
            name='Location 1',
            description='Description 1',
            address1='123 Fake St.',
            address2='#1234',
            city='Dallas',
            state='Texas',
            zip_code=12345,
            country='United States of America',
            latitude=123.345,
            longitude=123.345,
            direction_url='https://maps.com/direction/to/location')
        self.db.session.add(location)
        self.db.session.commit()

        response = self.client_open(
            '/api/location/1', 
            'DELETE')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(LocationModel.query.all()), 0)


class ProductCategoryTest(ApiTests):
    
    def test_post(self):
        payload = {'name': 'Product Category'}

        response = self.client_open(
            '/api/product_categories', 
            'POST', 
            data=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(str, type(response.json['name']))
        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['name'], 'Product Category')

    def test_get_all(self):
        category = ProductCategoryModel(name='Test Name 1')
        self.db.session.add(category)
        self.db.session.commit()

        category = ProductCategoryModel(name='Test Name 2')
        self.db.session.add(category)
        self.db.session.commit()

        response = self.client_open(
            '/api/product_categories', 
            'GET')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list, type(response.json))
        self.assertEqual(len(response.json), 2)
        self.assertEqual(int, type(response.json[0]['id']))
        self.assertEqual(str, type(response.json[0]['name']))
        self.assertEqual(dict, type(response.json[0]))
        self.assertEqual(response.json[0]['id'], 1)
        self.assertEqual(response.json[0]['name'], 'Test Name 1')

    def test_get_one(self):
        category = ProductCategoryModel(name='Test Name 1')
        self.db.session.add(category)
        self.db.session.commit()

        response = self.client_open(
            '/api/product_category/1', 
            'GET')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(dict, type(response.json))
        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(str, type(response.json['name']))
        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['name'], 'Test Name 1')

    def test_put_one(self):
        category = ProductCategoryModel(name='Test Name 1')
        self.db.session.add(category)
        self.db.session.commit()

        response = self.client_open(
            '/api/product_category/1', 
            'PUT',
            {'name': 'Changed Blog Category'})

        self.assertEqual(response.status_code, 201)
        self.assertEqual(dict, type(response.json))
        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(str, type(response.json['name']))
        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['name'], 'Changed Blog Category')

    def test_delete_one(self):
        category = ProductCategoryModel(name='Test Name 1')
        self.db.session.add(category)
        self.db.session.commit()

        response = self.client_open(
            '/api/product_category/1', 
            'DELETE')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(ProductCategoryModel.query.all()), 0)

class ProductTest(ApiTests):
    
    def test_post(self):
        category  = ProductCategoryModel(name='Product Category')
        self.db.session.add(category)
        self.db.session.commit()

        payload = {
            'name': 'Product Name',
            'short_description': 'Product Short Description',
            'long_description': 'Product Long Description',
            'product_category_id': 1,
            'img_path_xs': 'path/to/img_path_xs',
            'img_path_sm': 'path/to/img_path_sm',
            'img_path_md': 'path/to/img_path_md',
            'img_path_lg': 'path/to/img_path_lg'
        }

        response = self.client_open(
            '/api/products', 
            'POST', 
            data=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(str, type(response.json['name']))
        self.assertEqual(str, type(response.json['short_description']))
        self.assertEqual(str, type(response.json['long_description']))
        self.assertEqual(dict, type(response.json['product_category']))
        self.assertEqual(int, type(response.json['product_category']['id']))
        self.assertEqual(str, type(response.json['product_category']['name']))
        self.assertEqual(dict, type(response.json['images']))
        self.assertEqual(str, type(response.json['images']['img_path_xs']))
        self.assertEqual(str, type(response.json['images']['img_path_sm']))
        self.assertEqual(str, type(response.json['images']['img_path_md']))
        self.assertEqual(str, type(response.json['images']['img_path_lg']))

        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['name'], 'Product Name')
        self.assertEqual(response.json['short_description'], 'Product Short Description')
        self.assertEqual(response.json['long_description'], 'Product Long Description')
        self.assertEqual(response.json['product_category']['id'], 1)
        self.assertEqual(response.json['product_category']['name'], 'Product Category')
        self.assertEqual(response.json['images']['img_path_xs'], 'path/to/img_path_xs')
        self.assertEqual(response.json['images']['img_path_sm'], 'path/to/img_path_sm')
        self.assertEqual(response.json['images']['img_path_md'], 'path/to/img_path_md')
        self.assertEqual(response.json['images']['img_path_lg'], 'path/to/img_path_lg')

    def test_get_all(self):
        category = ProductCategoryModel(name='Test Name 1')
        self.db.session.add(category)
        self.db.session.commit()

        product  = ProductModel(
            name='Product Name',
            short_description='Product Short Description',
            long_description='Product Long Description',
            product_category_id=1,
            img_path_xs='path/to/img_path_xs',
            img_path_sm='path/to/img_path_sm',
            img_path_md='path/to/img_path_md',
            img_path_lg='path/to/img_path_lg'
            )
        self.db.session.add(product)
        self.db.session.commit()

        response = self.client_open(
            '/api/products', 
            'GET')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list, type(response.json))
        self.assertEqual(len(response.json), 1)
        self.assertEqual(int, type(response.json[0]['id']))
        self.assertEqual(str, type(response.json[0]['name']))
        self.assertEqual(str, type(response.json[0]['short_description']))
        self.assertEqual(str, type(response.json[0]['long_description']))
        self.assertEqual(dict, type(response.json[0]['product_category']))
        self.assertEqual(int, type(response.json[0]['product_category']['id']))
        self.assertEqual(str, type(response.json[0]['product_category']['name']))
        self.assertEqual(dict, type(response.json[0]['images']))
        self.assertEqual(str, type(response.json[0]['images']['img_path_xs']))
        self.assertEqual(str, type(response.json[0]['images']['img_path_sm']))
        self.assertEqual(str, type(response.json[0]['images']['img_path_md']))
        self.assertEqual(str, type(response.json[0]['images']['img_path_lg']))

        self.assertEqual(response.json[0]['id'], 1)
        self.assertEqual(response.json[0]['name'], 'Product Name')
        self.assertEqual(response.json[0]['short_description'], 'Product Short Description')
        self.assertEqual(response.json[0]['long_description'], 'Product Long Description')
        self.assertEqual(response.json[0]['product_category']['id'], 1)
        self.assertEqual(response.json[0]['product_category']['name'], 'Test Name 1')
        self.assertEqual(response.json[0]['images']['img_path_xs'], 'path/to/img_path_xs')
        self.assertEqual(response.json[0]['images']['img_path_sm'], 'path/to/img_path_sm')
        self.assertEqual(response.json[0]['images']['img_path_md'], 'path/to/img_path_md')
        self.assertEqual(response.json[0]['images']['img_path_lg'], 'path/to/img_path_lg')

    def test_get_one(self):
        category = ProductCategoryModel(name='Test Name 1')
        self.db.session.add(category)
        self.db.session.commit()

        product  = ProductModel(
            name='Product Name',
            short_description='Product Short Description',
            long_description='Product Long Description',
            product_category_id=1,
            img_path_xs='path/to/img_path_xs',
            img_path_sm='path/to/img_path_sm',
            img_path_md='path/to/img_path_md',
            img_path_lg='path/to/img_path_lg'
            )
        self.db.session.add(product)
        self.db.session.commit()

        response = self.client_open(
            '/api/product/1', 
            'GET')

        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(str, type(response.json['name']))
        self.assertEqual(str, type(response.json['short_description']))
        self.assertEqual(str, type(response.json['long_description']))
        self.assertEqual(dict, type(response.json['product_category']))
        self.assertEqual(int, type(response.json['product_category']['id']))
        self.assertEqual(str, type(response.json['product_category']['name']))
        self.assertEqual(dict, type(response.json['images']))
        self.assertEqual(str, type(response.json['images']['img_path_xs']))
        self.assertEqual(str, type(response.json['images']['img_path_sm']))
        self.assertEqual(str, type(response.json['images']['img_path_md']))
        self.assertEqual(str, type(response.json['images']['img_path_lg']))

        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['name'], 'Product Name')
        self.assertEqual(response.json['short_description'], 'Product Short Description')
        self.assertEqual(response.json['long_description'], 'Product Long Description')
        self.assertEqual(response.json['product_category']['id'], 1)
        self.assertEqual(response.json['product_category']['name'], 'Test Name 1')
        self.assertEqual(response.json['images']['img_path_xs'], 'path/to/img_path_xs')
        self.assertEqual(response.json['images']['img_path_sm'], 'path/to/img_path_sm')
        self.assertEqual(response.json['images']['img_path_md'], 'path/to/img_path_md')
        self.assertEqual(response.json['images']['img_path_lg'], 'path/to/img_path_lg')

    def test_put_one(self):
        category = ProductCategoryModel(name='Product Category')
        self.db.session.add(category)
        self.db.session.commit()

        product  = ProductModel(
            name='Product Name',
            short_description='Product Short Description',
            long_description='Product Long Description',
            product_category_id=1,
            img_path_xs='path/to/img_path_xs',
            img_path_sm='path/to/img_path_sm',
            img_path_md='path/to/img_path_md',
            img_path_lg='path/to/img_path_lg'
            )
        self.db.session.add(product)
        self.db.session.commit()

        response = self.client_open(
            '/api/product/1', 
            'PUT',
            {
                'name': 'changed Product Name',
                'short_description': 'Product Short Description',
                'long_description': 'Product Long Description',
                'product_category_id': 1,
                'img_path_xs': 'path/to/img_path_xs',
                'img_path_sm': 'path/to/img_path_sm',
                'img_path_md': 'path/to/img_path_md',
                'img_path_lg': 'path/to/img_path_lg'
            })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(dict, type(response.json))
        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(str, type(response.json['name']))
        self.assertEqual(str, type(response.json['short_description']))
        self.assertEqual(str, type(response.json['long_description']))
        self.assertEqual(dict, type(response.json['product_category']))
        self.assertEqual(int, type(response.json['product_category']['id']))
        self.assertEqual(str, type(response.json['product_category']['name']))
        self.assertEqual(dict, type(response.json['images']))
        self.assertEqual(str, type(response.json['images']['img_path_xs']))
        self.assertEqual(str, type(response.json['images']['img_path_sm']))
        self.assertEqual(str, type(response.json['images']['img_path_md']))
        self.assertEqual(str, type(response.json['images']['img_path_lg']))

        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['name'], 'changed Product Name')
        self.assertEqual(response.json['short_description'], 'Product Short Description')
        self.assertEqual(response.json['long_description'], 'Product Long Description')
        self.assertEqual(response.json['product_category']['id'], 1)
        self.assertEqual(response.json['product_category']['name'], 'Product Category')
        self.assertEqual(response.json['images']['img_path_xs'], 'path/to/img_path_xs')
        self.assertEqual(response.json['images']['img_path_sm'], 'path/to/img_path_sm')
        self.assertEqual(response.json['images']['img_path_md'], 'path/to/img_path_md')
        self.assertEqual(response.json['images']['img_path_lg'], 'path/to/img_path_lg')

    def test_delete_one(self):
        category = ProductCategoryModel(name='Test Name 1')
        self.db.session.add(category)
        self.db.session.commit()

        response = self.client_open(
            '/api/product_category/1', 
            'DELETE')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(ProductModel.query.all()), 0)


class LocationProductTest(ApiTests):
    
    def test_post(self):
        category = ProductCategoryModel(name='Product Category')
        self.db.session.add(category)
        self.db.session.commit()

        product  = ProductModel(
            name='Product Name',
            short_description='Product Short Description',
            long_description='Product Long Description',
            product_category_id=1,
            img_path_xs='path/to/img_path_xs',
            img_path_sm='path/to/img_path_sm',
            img_path_md='path/to/img_path_md',
            img_path_lg='path/to/img_path_lg'
            )
        self.db.session.add(product)
        self.db.session.commit()

        location  = LocationModel(
            name='Location 1',
            description='Description 1',
            address1='123 Fake St.',
            address2='#1234',
            city='Dallas',
            state='Texas',
            zip_code=12345,
            country='United States of America',
            latitude=123.345,
            longitude=123.345,
            direction_url='https://maps.com/direction/to/location')
        self.db.session.add(location)
        self.db.session.commit()


        payload = {
            'location_id': 1,
            'product_id': 1,
            'price': 12.34,
            'num_available': 50,
        }

        response = self.client_open(
            '/api/location_products', 
            'POST', 
            data=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(float, type(response.json['price']))
        self.assertEqual(int, type(response.json['num_available']))
        self.assertEqual(str, type(response.json['product']['name']))
        self.assertEqual(str, type(response.json['product']['short_description']))
        self.assertEqual(str, type(response.json['product']['long_description']))
        self.assertEqual(dict, type(response.json['product']['product_category']))
        self.assertEqual(int, type(response.json['product']['product_category']['id']))
        self.assertEqual(str, type(response.json['product']['product_category']['name']))
        self.assertEqual(dict, type(response.json['product']['images']))
        self.assertEqual(str, type(response.json['product']['images']['img_path_xs']))
        self.assertEqual(str, type(response.json['product']['images']['img_path_sm']))
        self.assertEqual(str, type(response.json['product']['images']['img_path_md']))
        self.assertEqual(str, type(response.json['product']['images']['img_path_lg']))
        self.assertEqual(int, type(response.json['location']['id']))
        self.assertEqual(str, type(response.json['location']['name']))
        self.assertEqual(str, type(response.json['location']['description']))
        self.assertEqual(str, type(response.json['location']['location']['address1']))
        self.assertEqual(str, type(response.json['location']['location']['address2']))
        self.assertEqual(str, type(response.json['location']['location']['city']))
        self.assertEqual(str, type(response.json['location']['location']['zip_code']))
        self.assertEqual(str, type(response.json['location']['location']['state']))
        self.assertEqual(str, type(response.json['location']['location']['country']))
        self.assertEqual(float, type(response.json['location']['location']['coordinates']['latitude']))
        self.assertEqual(float, type(response.json['location']['location']['coordinates']['longitude']))
        self.assertEqual(str, type(response.json['location']['direction_url']))


        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['price'], 12.34)
        self.assertEqual(response.json['num_available'], 50)

        self.assertEqual(response.json['product']['id'], 1)
        self.assertEqual(response.json['product']['name'],'Product Name')
        self.assertEqual(response.json['product']['short_description'], 'Product Short Description')
        self.assertEqual(response.json['product']['long_description'], 'Product Long Description')
        self.assertEqual(response.json['product']['product_category']['id'], 1)
        self.assertEqual(response.json['product']['product_category']['name'], 'Product Category')
        self.assertEqual(response.json['product']['images']['img_path_xs'], 'path/to/img_path_xs')
        self.assertEqual(response.json['product']['images']['img_path_sm'], 'path/to/img_path_sm')
        self.assertEqual(response.json['product']['images']['img_path_md'], 'path/to/img_path_md')
        self.assertEqual(response.json['product']['images']['img_path_lg'], 'path/to/img_path_lg')

        self.assertEqual(response.json['location']['id'], 1)
        self.assertEqual(response.json['location']['name'], 'Location 1')
        self.assertEqual(response.json['location']['description'], 'Description 1',)
        self.assertEqual(response.json['location']['location']['address1'], '123 Fake St.')
        self.assertEqual(response.json['location']['location']['address2'], '#1234')
        self.assertEqual(response.json['location']['location']['city'], 'Dallas')
        self.assertEqual(response.json['location']['location']['zip_code'], '12345')
        self.assertEqual(response.json['location']['location']['state'], 'Texas')
        self.assertEqual(response.json['location']['location']['country'], 'United States of America')
        self.assertEqual(response.json['location']['location']['coordinates']['latitude'], 123.345)
        self.assertEqual(response.json['location']['location']['coordinates']['longitude'], 123.345)
        self.assertEqual(response.json['location']['direction_url'], 'https://maps.com/direction/to/location')


    def test_get_all(self):
        category = ProductCategoryModel(name='Product Category')
        self.db.session.add(category)
        self.db.session.commit()

        product  = ProductModel(
            name='Product Name',
            short_description='Product Short Description',
            long_description='Product Long Description',
            product_category_id=1,
            img_path_xs='path/to/img_path_xs',
            img_path_sm='path/to/img_path_sm',
            img_path_md='path/to/img_path_md',
            img_path_lg='path/to/img_path_lg'
            )
        self.db.session.add(product)
        self.db.session.commit()

        location  = LocationModel(
            name='Location 1',
            description='Description 1',
            address1='123 Fake St.',
            address2='#1234',
            city='Dallas',
            state='Texas',
            zip_code=12345,
            country='United States of America',
            latitude=123.345,
            longitude=123.345,
            direction_url='https://maps.com/direction/to/location')
        self.db.session.add(location)
        self.db.session.commit()

        location_product = LocationProductModel(
            location_id=1,
            product_id=1,
            price=12.34,
            num_available=50)
        self.db.session.add(location_product)
        self.db.session.commit()

        response = self.client_open(
            '/api/location_products', 
            'GET')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list, type(response.json))
        self.assertEqual(len(response.json), 1)

        self.assertEqual(int, type(response.json[0]['id']))
        self.assertEqual(float, type(response.json[0]['price']))
        self.assertEqual(int, type(response.json[0]['num_available']))
        self.assertEqual(str, type(response.json[0]['product']['name']))
        self.assertEqual(str, type(response.json[0]['product']['short_description']))
        self.assertEqual(str, type(response.json[0]['product']['long_description']))
        self.assertEqual(dict, type(response.json[0]['product']['product_category']))
        self.assertEqual(int, type(response.json[0]['product']['product_category']['id']))
        self.assertEqual(str, type(response.json[0]['product']['product_category']['name']))
        self.assertEqual(dict, type(response.json[0]['product']['images']))
        self.assertEqual(str, type(response.json[0]['product']['images']['img_path_xs']))
        self.assertEqual(str, type(response.json[0]['product']['images']['img_path_sm']))
        self.assertEqual(str, type(response.json[0]['product']['images']['img_path_md']))
        self.assertEqual(str, type(response.json[0]['product']['images']['img_path_lg']))
        self.assertEqual(int, type(response.json[0]['location']['id']))
        self.assertEqual(str, type(response.json[0]['location']['name']))
        self.assertEqual(str, type(response.json[0]['location']['description']))
        self.assertEqual(str, type(response.json[0]['location']['location']['address1']))
        self.assertEqual(str, type(response.json[0]['location']['location']['address2']))
        self.assertEqual(str, type(response.json[0]['location']['location']['city']))
        self.assertEqual(str, type(response.json[0]['location']['location']['zip_code']))
        self.assertEqual(str, type(response.json[0]['location']['location']['state']))
        self.assertEqual(str, type(response.json[0]['location']['location']['country']))
        self.assertEqual(float, type(response.json[0]['location']['location']['coordinates']['latitude']))
        self.assertEqual(float, type(response.json[0]['location']['location']['coordinates']['longitude']))
        self.assertEqual(str, type(response.json[0]['location']['direction_url']))


        self.assertEqual(response.json[0]['id'], 1)
        self.assertEqual(response.json[0]['price'], 12.34)
        self.assertEqual(response.json[0]['num_available'], 50)

        self.assertEqual(response.json[0]['product']['id'], 1)
        self.assertEqual(response.json[0]['product']['name'],'Product Name')
        self.assertEqual(response.json[0]['product']['short_description'], 'Product Short Description')
        self.assertEqual(response.json[0]['product']['long_description'], 'Product Long Description')
        self.assertEqual(response.json[0]['product']['product_category']['id'], 1)
        self.assertEqual(response.json[0]['product']['product_category']['name'], 'Product Category')
        self.assertEqual(response.json[0]['product']['images']['img_path_xs'], 'path/to/img_path_xs')
        self.assertEqual(response.json[0]['product']['images']['img_path_sm'], 'path/to/img_path_sm')
        self.assertEqual(response.json[0]['product']['images']['img_path_md'], 'path/to/img_path_md')
        self.assertEqual(response.json[0]['product']['images']['img_path_lg'], 'path/to/img_path_lg')

        self.assertEqual(response.json[0]['location']['id'], 1)
        self.assertEqual(response.json[0]['location']['name'], 'Location 1')
        self.assertEqual(response.json[0]['location']['description'], 'Description 1',)
        self.assertEqual(response.json[0]['location']['location']['address1'], '123 Fake St.')
        self.assertEqual(response.json[0]['location']['location']['address2'], '#1234')
        self.assertEqual(response.json[0]['location']['location']['city'], 'Dallas')
        self.assertEqual(response.json[0]['location']['location']['zip_code'], '12345')
        self.assertEqual(response.json[0]['location']['location']['state'], 'Texas')
        self.assertEqual(response.json[0]['location']['location']['country'], 'United States of America')
        self.assertEqual(response.json[0]['location']['location']['coordinates']['latitude'], 123.345)
        self.assertEqual(response.json[0]['location']['location']['coordinates']['longitude'], 123.345)
        self.assertEqual(response.json[0]['location']['direction_url'], 'https://maps.com/direction/to/location')


    def test_get_one(self):
        category = ProductCategoryModel(name='Product Category')
        self.db.session.add(category)
        self.db.session.commit()

        product  = ProductModel(
            name='Product Name',
            short_description='Product Short Description',
            long_description='Product Long Description',
            product_category_id=1,
            img_path_xs='path/to/img_path_xs',
            img_path_sm='path/to/img_path_sm',
            img_path_md='path/to/img_path_md',
            img_path_lg='path/to/img_path_lg'
            )
        self.db.session.add(product)
        self.db.session.commit()

        location  = LocationModel(
            name='Location 1',
            description='Description 1',
            address1='123 Fake St.',
            address2='#1234',
            city='Dallas',
            state='Texas',
            zip_code=12345,
            country='United States of America',
            latitude=123.345,
            longitude=123.345,
            direction_url='https://maps.com/direction/to/location')
        self.db.session.add(location)
        self.db.session.commit()

        location_product = LocationProductModel(
            location_id=1,
            product_id=1,
            price=12.34,
            num_available=50)
        self.db.session.add(location_product)
        self.db.session.commit()

        response = self.client_open(
            '/api/location_product/1', 
            'GET')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(dict, type(response.json))
        self.assertEqual(len(response.json), 5)

        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(float, type(response.json['price']))
        self.assertEqual(int, type(response.json['num_available']))
        self.assertEqual(str, type(response.json['product']['name']))
        self.assertEqual(str, type(response.json['product']['short_description']))
        self.assertEqual(str, type(response.json['product']['long_description']))
        self.assertEqual(dict, type(response.json['product']['product_category']))
        self.assertEqual(int, type(response.json['product']['product_category']['id']))
        self.assertEqual(str, type(response.json['product']['product_category']['name']))
        self.assertEqual(dict, type(response.json['product']['images']))
        self.assertEqual(str, type(response.json['product']['images']['img_path_xs']))
        self.assertEqual(str, type(response.json['product']['images']['img_path_sm']))
        self.assertEqual(str, type(response.json['product']['images']['img_path_md']))
        self.assertEqual(str, type(response.json['product']['images']['img_path_lg']))
        self.assertEqual(int, type(response.json['location']['id']))
        self.assertEqual(str, type(response.json['location']['name']))
        self.assertEqual(str, type(response.json['location']['description']))
        self.assertEqual(str, type(response.json['location']['location']['address1']))
        self.assertEqual(str, type(response.json['location']['location']['address2']))
        self.assertEqual(str, type(response.json['location']['location']['city']))
        self.assertEqual(str, type(response.json['location']['location']['zip_code']))
        self.assertEqual(str, type(response.json['location']['location']['state']))
        self.assertEqual(str, type(response.json['location']['location']['country']))
        self.assertEqual(float, type(response.json['location']['location']['coordinates']['latitude']))
        self.assertEqual(float, type(response.json['location']['location']['coordinates']['longitude']))
        self.assertEqual(str, type(response.json['location']['direction_url']))


        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['price'], 12.34)
        self.assertEqual(response.json['num_available'], 50)

        self.assertEqual(response.json['product']['id'], 1)
        self.assertEqual(response.json['product']['name'],'Product Name')
        self.assertEqual(response.json['product']['short_description'], 'Product Short Description')
        self.assertEqual(response.json['product']['long_description'], 'Product Long Description')
        self.assertEqual(response.json['product']['product_category']['id'], 1)
        self.assertEqual(response.json['product']['product_category']['name'], 'Product Category')
        self.assertEqual(response.json['product']['images']['img_path_xs'], 'path/to/img_path_xs')
        self.assertEqual(response.json['product']['images']['img_path_sm'], 'path/to/img_path_sm')
        self.assertEqual(response.json['product']['images']['img_path_md'], 'path/to/img_path_md')
        self.assertEqual(response.json['product']['images']['img_path_lg'], 'path/to/img_path_lg')

        self.assertEqual(response.json['location']['id'], 1)
        self.assertEqual(response.json['location']['name'], 'Location 1')
        self.assertEqual(response.json['location']['description'], 'Description 1')
        self.assertEqual(response.json['location']['location']['address1'], '123 Fake St.')
        self.assertEqual(response.json['location']['location']['address2'], '#1234')
        self.assertEqual(response.json['location']['location']['city'], 'Dallas')
        self.assertEqual(response.json['location']['location']['zip_code'], '12345')
        self.assertEqual(response.json['location']['location']['state'], 'Texas')
        self.assertEqual(response.json['location']['location']['country'], 'United States of America')
        self.assertEqual(response.json['location']['location']['coordinates']['latitude'], 123.345)
        self.assertEqual(response.json['location']['location']['coordinates']['longitude'], 123.345)
        self.assertEqual(response.json['location']['direction_url'], 'https://maps.com/direction/to/location')


    def test_put_one(self):
        category = ProductCategoryModel(name='Product Category')
        self.db.session.add(category)
        self.db.session.commit()

        product  = ProductModel(
            name='Product Name',
            short_description='Product Short Description',
            long_description='Product Long Description',
            product_category_id=1,
            img_path_xs='path/to/img_path_xs',
            img_path_sm='path/to/img_path_sm',
            img_path_md='path/to/img_path_md',
            img_path_lg='path/to/img_path_lg'
            )
        self.db.session.add(product)
        self.db.session.commit()

        location  = LocationModel(
            name='Location 1',
            description='Description 1',
            address1='123 Fake St.',
            address2='#1234',
            city='Dallas',
            state='Texas',
            zip_code=12345,
            country='United States of America',
            latitude=123.345,
            longitude=123.345,
            direction_url='https://maps.com/direction/to/location')
        self.db.session.add(location)
        self.db.session.commit()

        location_product = LocationProductModel(
            location_id=1,
            product_id=1,
            price=12.34,
            num_available=50)
        self.db.session.add(location_product)
        self.db.session.commit()

        response = self.client_open(
            '/api/location_product/1', 
            'PUT',
            {
                'location_id': 1,
                'product_id': 1,
                'price': 12.34,
                'num_available': 50
            })

        self.assertEqual(response.status_code, 201)
        self.assertEqual(dict, type(response.json))
        self.assertEqual(len(response.json), 5)

        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(float, type(response.json['price']))
        self.assertEqual(int, type(response.json['num_available']))
        self.assertEqual(str, type(response.json['product']['name']))
        self.assertEqual(str, type(response.json['product']['short_description']))
        self.assertEqual(str, type(response.json['product']['long_description']))
        self.assertEqual(dict, type(response.json['product']['product_category']))
        self.assertEqual(int, type(response.json['product']['product_category']['id']))
        self.assertEqual(str, type(response.json['product']['product_category']['name']))
        self.assertEqual(dict, type(response.json['product']['images']))
        self.assertEqual(str, type(response.json['product']['images']['img_path_xs']))
        self.assertEqual(str, type(response.json['product']['images']['img_path_sm']))
        self.assertEqual(str, type(response.json['product']['images']['img_path_md']))
        self.assertEqual(str, type(response.json['product']['images']['img_path_lg']))
        self.assertEqual(int, type(response.json['location']['id']))
        self.assertEqual(str, type(response.json['location']['name']))
        self.assertEqual(str, type(response.json['location']['description']))
        self.assertEqual(str, type(response.json['location']['location']['address1']))
        self.assertEqual(str, type(response.json['location']['location']['address2']))
        self.assertEqual(str, type(response.json['location']['location']['city']))
        self.assertEqual(str, type(response.json['location']['location']['zip_code']))
        self.assertEqual(str, type(response.json['location']['location']['state']))
        self.assertEqual(str, type(response.json['location']['location']['country']))
        self.assertEqual(float, type(response.json['location']['location']['coordinates']['latitude']))
        self.assertEqual(float, type(response.json['location']['location']['coordinates']['longitude']))
        self.assertEqual(str, type(response.json['location']['direction_url']))


        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['price'], 12.34)
        self.assertEqual(response.json['num_available'], 50)

        self.assertEqual(response.json['product']['id'], 1)
        self.assertEqual(response.json['product']['name'],'Product Name')
        self.assertEqual(response.json['product']['short_description'], 'Product Short Description')
        self.assertEqual(response.json['product']['long_description'], 'Product Long Description')
        self.assertEqual(response.json['product']['product_category']['id'], 1)
        self.assertEqual(response.json['product']['product_category']['name'], 'Product Category')
        self.assertEqual(response.json['product']['images']['img_path_xs'], 'path/to/img_path_xs')
        self.assertEqual(response.json['product']['images']['img_path_sm'], 'path/to/img_path_sm')
        self.assertEqual(response.json['product']['images']['img_path_md'], 'path/to/img_path_md')
        self.assertEqual(response.json['product']['images']['img_path_lg'], 'path/to/img_path_lg')

        self.assertEqual(response.json['location']['id'], 1)
        self.assertEqual(response.json['location']['name'], 'Location 1')
        self.assertEqual(response.json['location']['description'], 'Description 1')
        self.assertEqual(response.json['location']['location']['address1'], '123 Fake St.')
        self.assertEqual(response.json['location']['location']['address2'], '#1234')
        self.assertEqual(response.json['location']['location']['city'], 'Dallas')
        self.assertEqual(response.json['location']['location']['zip_code'], '12345')
        self.assertEqual(response.json['location']['location']['state'], 'Texas')
        self.assertEqual(response.json['location']['location']['country'], 'United States of America')
        self.assertEqual(response.json['location']['location']['coordinates']['latitude'], 123.345)
        self.assertEqual(response.json['location']['location']['coordinates']['longitude'], 123.345)
        self.assertEqual(response.json['location']['direction_url'], 'https://maps.com/direction/to/location')

    def test_delete_one(self):
        category = ProductCategoryModel(name='Product Category')
        self.db.session.add(category)
        self.db.session.commit()

        product  = ProductModel(
            name='Product Name',
            short_description='Product Short Description',
            long_description='Product Long Description',
            product_category_id=1,
            img_path_xs='path/to/img_path_xs',
            img_path_sm='path/to/img_path_sm',
            img_path_md='path/to/img_path_md',
            img_path_lg='path/to/img_path_lg'
            )
        self.db.session.add(product)
        self.db.session.commit()

        location  = LocationModel(
            name='Location 1',
            description='Description 1',
            address1='123 Fake St.',
            address2='#1234',
            city='Dallas',
            state='Texas',
            zip_code=12345,
            country='United States of America',
            latitude=123.345,
            longitude=123.345,
            direction_url='https://maps.com/direction/to/location')
        self.db.session.add(location)
        self.db.session.commit()

        location_product = LocationProductModel(
            location_id=1,
            product_id=1,
            price=12.34,
            num_available=50)
        self.db.session.add(location_product)
        self.db.session.commit()

        response = self.client_open(
            '/api/location_product/1', 
            'DELETE')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(LocationProductModel.query.all()), 0)

class RoleTest(ApiTests):
    def test_post(self):
        payload = {
            'name': 'Name',
            'description': 'Description',
        }

        response = self.client_open(
            '/api/roles', 
            'POST', 
            data=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.json), 3)
        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(str, type(response.json['name']))
        self.assertEqual(str, type(response.json['description']))

        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['name'], 'Name')
        self.assertEqual(response.json['description'], 'Description')

    def test_get_all(self):
        role  = RoleModel(
            name='Name',
            description='Description')
        self.db.session.add(role)
        self.db.session.commit()

        response = self.client_open(
            '/api/roles', 
            'GET')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list, type(response.json))
        self.assertEqual(dict, type(response.json[0]))

        self.assertEqual(int, type(response.json[0]['id']))
        self.assertEqual(str, type(response.json[0]['name']))
        self.assertEqual(str, type(response.json[0]['description']))

        self.assertEqual(response.json[0]['id'], 1)
        self.assertEqual(response.json[0]['name'], 'Name')
        self.assertEqual(response.json[0]['description'], 'Description')


    def test_get_one(self):
        role  = RoleModel(
            name='Name',
            description='Description')
        self.db.session.add(role)
        self.db.session.commit()

        response = self.client_open(
            '/api/role/1', 
            'GET')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(dict, type(response.json))

        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(str, type(response.json['name']))
        self.assertEqual(str, type(response.json['description']))

        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['name'], 'Name')
        self.assertEqual(response.json['description'], 'Description')

    def test_put_one(self):
        role  = RoleModel(
            name='Name',
            description='Description')
        self.db.session.add(role)
        self.db.session.commit()

        response = self.client_open(
            '/api/role/1', 
            'PUT',
            {
                'name': 'changed name',
                'description': 'changed description',
            })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(dict, type(response.json))
        self.assertEqual(len(response.json), 3)

        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(str, type(response.json['name']))
        self.assertEqual(str, type(response.json['description']))

        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['name'], 'changed name')
        self.assertEqual(response.json['description'], 'changed description')

    def test_delete_one(self):
        role  = RoleModel(
            name='Name',
            description='Description')
        self.db.session.add(role)
        self.db.session.commit()

        response = self.client_open(
            '/api/role/1', 
            'DELETE')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(HelpArticleModel.query.all()), 0)




class UserTest(ApiTests):
    def test_post(self):
        role  = RoleModel(
            name='Name',
            description='Description')
        self.db.session.add(role)
        self.db.session.commit()

        payload = {
            'name': 'John Doe',
            'phone': '1235551234',
            'email': 'john_doe@example.com',
            'password': 'Password123#',
            'confirmed_at': datetime.datetime(2018, 11, 28),
            'role_id': 1
        }

        response = self.client_open(
            '/api/users',
            'POST', 
            data=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.json), 9)
        self.assertEqual(len(response.json['role']), 3)

        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(str, type(response.json['name']))
        self.assertEqual(str, type(response.json['phone']))
        self.assertEqual(str, type(response.json['email']))
        self.assertEqual(str, type(response.json['salted_hashed_password']))
        self.assertEqual(bool, type(response.json['active']))
        self.assertEqual(bool, type(response.json['banned']))
        self.assertEqual(str, type(response.json['confirmed_at']))
        self.assertEqual(dict, type(response.json['role']))

        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['name'], 'John Doe')
        self.assertEqual(response.json['phone'], '1235551234')
        self.assertEqual(response.json['email'], 'john_doe@example.com')
        self.assertNotEqual(response.json['salted_hashed_password'], 'Password123#') 
        self.assertEqual(response.json['active'], False)
        self.assertEqual(response.json['banned'], False)
        self.assertEqual(response.json['confirmed_at'], datetime.datetime(2018, 11, 28).isoformat())
        self.assertEqual(response.json['role']['id'], 1)
        self.assertEqual(response.json['role']['name'], 'Name')
        self.assertEqual(response.json['role']['description'], 'Description')

    def test_get_all(self):
        role  = RoleModel(
            name='Name',
            description='Description')
        self.db.session.add(role)
        self.db.session.commit()

        user = UserModel(
            name='John Doe',
            phone='1235551234',
            email='john_doe@example.com',
            password='Password123#',
            confirmed_at=datetime.datetime(2018, 11, 28),
            role_id=1)
        self.db.session.add(user)
        self.db.session.commit()

        response = self.client_open(
            '/api/users', 
            'GET')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list, type(response.json))
        self.assertEqual(dict, type(response.json[0]))

        self.assertEqual(int, type(response.json[0]['id']))
        self.assertEqual(str, type(response.json[0]['name']))
        self.assertEqual(str, type(response.json[0]['phone']))
        self.assertEqual(str, type(response.json[0]['email']))
        self.assertEqual(str, type(response.json[0]['salted_hashed_password']))
        self.assertEqual(bool, type(response.json[0]['active']))
        self.assertEqual(bool, type(response.json[0]['banned']))
        self.assertEqual(str, type(response.json[0]['confirmed_at']))
        self.assertEqual(dict, type(response.json[0]['role']))

        self.assertEqual(response.json[0]['id'], 1)
        self.assertEqual(response.json[0]['name'], 'John Doe')
        self.assertEqual(response.json[0]['phone'], '1235551234')
        self.assertEqual(response.json[0]['email'], 'john_doe@example.com')
        self.assertNotEqual(response.json[0]['salted_hashed_password'], 'Password123#')
        self.assertEqual(response.json[0]['active'], False)
        self.assertEqual(response.json[0]['banned'], False)
        self.assertEqual(response.json[0]['confirmed_at'], datetime.datetime(2018, 11, 28).isoformat())
        self.assertEqual(response.json[0]['role']['id'], 1)
        self.assertEqual(response.json[0]['role']['name'], 'Name')
        self.assertEqual(response.json[0]['role']['description'], 'Description')


    def test_get_one(self):
        role  = RoleModel(
            name='Name',
            description='Description')
        self.db.session.add(role)
        self.db.session.commit()

        user = UserModel(
            name='John Doe',
            phone='1235551234',
            email='john_doe@example.com',
            password='Password123#',
            confirmed_at=datetime.datetime(2018, 11, 28),
            role_id=1)
        self.db.session.add(user)
        self.db.session.commit()

        response = self.client_open(
            '/api/user/1', 
            'GET')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(dict, type(response.json))

        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(str, type(response.json['name']))
        self.assertEqual(str, type(response.json['phone']))
        self.assertEqual(str, type(response.json['email']))
        self.assertEqual(str, type(response.json['salted_hashed_password']))
        self.assertEqual(bool, type(response.json['active']))
        self.assertEqual(bool, type(response.json['banned']))
        self.assertEqual(str, type(response.json['confirmed_at']))
        self.assertEqual(dict, type(response.json['role']))

        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['name'], 'John Doe')
        self.assertEqual(response.json['phone'], '1235551234')
        self.assertEqual(response.json['email'], 'john_doe@example.com')
        self.assertNotEqual(response.json['salted_hashed_password'], 'Password123#')
        self.assertEqual(response.json['active'], False)
        self.assertEqual(response.json['banned'], False)
        self.assertEqual(response.json['confirmed_at'], datetime.datetime(2018, 11, 28).isoformat())
        self.assertEqual(response.json['role']['id'], 1)
        self.assertEqual(response.json['role']['name'], 'Name')
        self.assertEqual(response.json['role']['description'], 'Description')

    def test_put_one(self):
        role  = RoleModel(
            name='Name',
            description='Description')
        self.db.session.add(role)
        self.db.session.commit()

        user = UserModel(
            name='John Doe',
            phone='1235551234',
            email='john_doe@example.com',
            password='Password123#',
            confirmed_at=datetime.datetime(2018, 11, 28),
            role_id=1)
        self.db.session.add(user)
        self.db.session.commit()

        response = self.client_open(
            '/api/user/1', 
            'PUT',
            {
                'name': 'Jane Doe',
                'phone': '1235554321',
                'email': 'jane_doe@example.com',
                'password': 'NewPassword123#',
                'confirmed_at': datetime.datetime(2018, 11, 29),
                'role_id': 1,
                'active': True,
                'banned': True
            })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(dict, type(response.json))
        self.assertEqual(len(response.json), 9)

        self.assertEqual(int, type(response.json['id']))
        self.assertEqual(str, type(response.json['name']))
        self.assertEqual(str, type(response.json['phone']))
        self.assertEqual(str, type(response.json['email']))
        self.assertEqual(str, type(response.json['salted_hashed_password']))
        self.assertEqual(bool, type(response.json['active']))
        self.assertEqual(bool, type(response.json['banned']))
        self.assertEqual(str, type(response.json['confirmed_at']))
        self.assertEqual(dict, type(response.json['role']))

        self.assertEqual(response.json['id'], 1)
        self.assertEqual(response.json['name'], 'Jane Doe')
        self.assertEqual(response.json['phone'], '1235554321')
        self.assertEqual(response.json['email'], 'jane_doe@example.com')
        self.assertNotEqual(response.json['salted_hashed_password'], 'NewPassword123')
        self.assertEqual(response.json['active'], True)
        self.assertEqual(response.json['banned'], True)
        self.assertEqual(response.json['confirmed_at'], datetime.datetime(2018, 11, 29).isoformat())
        self.assertEqual(response.json['role']['id'], 1)
        self.assertEqual(response.json['role']['name'], 'Name')
        self.assertEqual(response.json['role']['description'], 'Description')

    def test_delete_one(self):
        role  = RoleModel(
            name='Name',
            description='Description')
        self.db.session.add(role)
        self.db.session.commit()

        user = UserModel(
            name='John Doe',
            phone='1235551234',
            email='john_doe@example.com',
            password='Password123#',
            confirmed_at=datetime.datetime(2018, 11, 28),
            role_id=1)
        self.db.session.add(user)
        self.db.session.commit()

        response = self.client_open(
            '/api/user/1', 
            'DELETE')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(HelpArticleModel.query.all()), 0)


if __name__ == '__main__':
    unittest.main()