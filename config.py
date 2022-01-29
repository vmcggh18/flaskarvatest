import os
class Config(object):
    DEBUG = False
    TESTING = False
    # this links to key in .env
    SECRET_KEY = os.environ.get('SECRET_KEY')
    EMAIL = os.environ.get('EMAIL')
    PASSWORD = os.environ.get('PASSWORD')

class ProductionConfig(Config):
    DEBUG=False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
