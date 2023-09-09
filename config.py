import os

class Config(object):
    DEBUG = False
    TESTING = False
    # this links to key in .env
    SECRET_KEY = os.environ.get('SECRET_KEY')
    EMAIL = os.environ.get('EMAIL')
    PASSWORD = os.environ.get('PASSWORD')
    # uri = os.environ["DATABASE_URL"]
    # if uri.startswith("postgres://"):
    #     uri = uri.replace("postgres://", "postgresql://", 1)
    # SQLALCHEMY_DATABASE_URI = uri
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

class ProductionConfig(Config):
    DEBUG=False
#     uri = os.environ.get("DATABASE_URL")  
#     if uri.startswith("postgres://"):
#         db_change = uri.replace("postgres://", "postgresql://", 1)
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' 
    

class TestingConfig(Config):
    TESTING = True
