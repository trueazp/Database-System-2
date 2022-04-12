import json

from app import db
from datetime import datetime
from flask_wtf import FlaskForm
from flask_login import UserMixin
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

# user object
class User(UserMixin, db.DynamicDocument):
  username = db.StringField(unique=True, required=True)
  email = db.StringField(unique=True, required=True)
  password = db.StringField(required=True)


# news object
class News(db.DynamicDocument):
  judul = db.StringField(required=True)
  penulis = db.StringField(required=True)
  tanggal = db.DateField(required=True)
  kategori = db.StringField(required=True)
  tags = db.ListField(field=db.StringField(), required=True)
  cover = db.FileField(required=True)
  rating = db.IntField(required=True)
  counter = db.IntField(required=True)
  detail = db.ListField(field=db.StringField(), required=True)


#  login form object
class LoginForm(FlaskForm):
  username = StringField(label='Username', validators=[InputRequired(), Length(min=4, max=20)])
  password = PasswordField(label='Password', validators=[InputRequired(), Length(max=80)])
  remember = BooleanField(label='Remember Me')


# registration form object
class RegistrationForm(FlaskForm):
  username = StringField(label='Username', validators=[InputRequired(), Length(min=4, max=20)])
  email = StringField(label='Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
  password = PasswordField(label='Password', validators=[InputRequired(), Length(min=8, max=80)])


# filter by date form object
class FilterByDateForm(FlaskForm):
  searchText = StringField(label='Filter News By Date', validators=[InputRequired()])


# filter by tag form object
class FilterByTagForm(FlaskForm):
  searchText = StringField(label='Filter News By Tag', validators=[InputRequired()])