from arvaghdraft import db, login_manager
from datetime import datetime
# UserMixin includes is_autheticated, etc
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# create models
# user model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # posts = db.relationship('Post', backref='author', lazy=True)
    

    def __repr__(self):
        return f"User('{self.username}', '{self.email}','{self.image_file}')"

# event model 
class Event(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    venue = db.Column(db.String(20), nullable=False)
    # eventtime = db.Column(db.DateTime, nullable=False)
    eventtime =  db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    message = db.Column(db.Text, nullable=False)
    approved_event =  db.Column(db.Boolean(), default=False, nullable=False, server_default='f')
    # link user to event
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # approve the event
    def approve(self):
        self.approved_event = True
    # determine what object looks like when printed out
    def __repr__(self):
        return f"Event'{self.title}', '{self.name}', '{self.date}', '{self.venue}','{self.date_posted}', '{self.message}', '{self.email}', '{self.approved_event}')"
