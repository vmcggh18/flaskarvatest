import dotenv
from flask import Flask
# from flask_fontawesome import FontAwesome
import os
import re
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


load_dotenv()

app = Flask(__name__)

app.config.from_object("config.DevelopmentConfig")
# uri = os.environ.get("DATABASE_URL")
# if uri.startswith("postgres://"):
#         uri = uri.replace("postgres://", "postgresql://", 1)
if app.config.from_object("config.DevelopmentConfig") == 'development':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
else:
    uri = os.environ["DATABASE_URL"]
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    # SQLALCHEMY_DATABASE_URI = uri
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')  
# get rid of deprecation error (however must be true if using whoosh for searching)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# initialise db to store model tables
db = SQLAlchemy(app)
# initialise bcrypt to hash passwords
bcrypt = Bcrypt(app)
# configure a loginmanager instance
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from arvaghdraft import views
from arvaghdraft import admin_views