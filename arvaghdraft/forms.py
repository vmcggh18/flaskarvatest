from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, PasswordField, validators
from wtforms.fields.datetime import DateField, TimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from wtforms.fields import DateField, EmailField, TelField
# imports for account page to cope with images
from flask_wtf.file import FileAllowed, FileField
from datetime import datetime, date

# from arvaghdraft.forms import RegistrationForm, LoginForm
from arvaghdraft.models import User, Event
from flask_login import current_user


class EventForm(FlaskForm):
    name = StringField("Name/Company: ", validators=[DataRequired()])
    email = StringField("email: ", validators=[Email(), Length(min=5)])
    title = StringField("Brief title: ", validators=[DataRequired()])
    date = DateField("Event Date: ")
    venue = StringField("Where / Venue: ")
    # eventtime =  TimeField("Start Time: ")
    eventtime =  StringField("Start Time: ")
    message = TextAreaField("More Detail of Event: ")
    submit = SubmitField("Click to Submit")
    

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(min=5)])
    password = PasswordField('Password', [validators.DataRequired()])  
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    # custom validators
    # function to prevent username duplication
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken! Please choose another one.')
      # function to prevent email duplication
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email address is already taken! Please choose another one.') 
        
        
class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[Email(), Length(min=5)])
    password = PasswordField('Password', [validators.DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update Profile')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')