import dotenv
from flask import Flask
# from flask_fontawesome import FontAwesome
from flask_mail import Mail
import os
import re
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
# username password location name
# postgresql://arva_test_db_example_user:U2YIM6p5ZYszdWlLwCvk9EYY54VEPvFg@dpg-ck63ad36fquc73c3dvog-a.frankfurt-postgres.render.com/arva_test_db_example

load_dotenv()

app = Flask(__name__)

app.config.from_object("config.DevelopmentConfig")
# use code block below when in development
if app.config.from_object("config.DevelopmentConfig") == 'development':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
else:
    uri = os.environ["DATABASE_URL"]
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    # line below not used
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')  
# use for local host 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# get rid of deprecation error (however must be true if using whoosh for searching
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# initialise db to store model tables
db = SQLAlchemy(app)
# initialise bcrypt to hash passwords
bcrypt = Bcrypt(app)
# configure a loginmanager instance
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465  # as using ssl
app.config['MAIL_USERNAME'] = 'arvaghonline@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False # True
app.config['MAIL_USE_SSL'] = True # False
# app.config['MAIL_DEBUG'] =  True
app.config['MAIL_DEFAULT_SENDER'] = 'arvaghonline@gmail.com'
app.config['MAIL_MAX_EMAILS'] = 5
# app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False
mail = Mail(app)


# check if db needs to be initialised
engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector = sa.inspect(engine)
if not inspector.has_table("event"):
    with app.app_context():
        db.drop_all()
        db.create_all

from arvaghdraft import views
from arvaghdraft import admin_views