""" Stores configuration for develoment, testing, and prodution flask app."""
import os

class Config(object):
    """Base configuration for Flask App"""

    PRESERVE_CONTEXT_ON_EXCEPTION = False
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('DiamondCaseWeb_secret_key', '1234567890')
    TESTING = False

    # Flask Mail Configurations
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('GMAIL_EMAIL')
    MAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')
  
    # Flask-S3 Configuration
    FLASKS3_USE_HTTPS = True
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    FLASKS3_BUCKET_NAME = os.environ.get('FLASKS3_BUCKET_NAME')
    FLASKS3_REGION = os.environ.get('FLASKS3_REGION')
    UPLOAD_FOLDER = '.static/upload'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

    # Flask Security Configurations
    SECURITY_POST_LOGIN='/profile'

    # Flask SQLAlchemy Configurations
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Flask-Social Configurations
    SOCIAL_TWITTER={'consumer_key': 'twitter consumer key',
                        'consumer_secret': 'twitter consumer secret'}
    SOCIAL_FACEBOOK={'consumer_key': 'facebook app id',
                     'consumer_secret': 'facebook app secret'}
    SOCIAL_FOURSQUARE={'consumer_key': 'client id',
                       'consumer_secret': 'client secret'}
    SOCIAL_GOOGLE={'consumer_key': 'xxxx',
                   'consumer_secret': 'xxxx'}

class ProductionConfig(Config):
    """Production configuration for Flask App"""
    # Flask SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI = 'postgresql://user@localhost/foo'

class DevelopmentConfig(Config):
    """Development configuration for Flask App"""
    # Flask Configuration
    DEBUG = True

    # Flask-S3 Configuration
    FLASKS3_DEBUG = True

    # Flask SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI='sqlite:////Users/jonathansullivan/DiamondCase/development.db'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    """Testing configuration for Flask App"""
    # Flask Configuration
    TESTING = True

    # Flask SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/jonathansullivan/DiamondCase/test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    SQLALCHEMY_RECORD_QUERIES = True
    
    