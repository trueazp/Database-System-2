import random

from app import db
from datetime import datetime
from flask_wtf import FlaskForm
from flask_admin import AdminIndexView
from flask import redirect, url_for, flash
from flask_login import UserMixin, current_user
from flask_admin.contrib.mongoengine import ModelView
from wtforms.validators import InputRequired, Email, Length
from wtforms import StringField, PasswordField, BooleanField, DateField, SelectField, FieldList, FileField, IntegerField, SubmitField

# user object
class User(UserMixin, db.DynamicDocument):
  username = db.StringField(unique=True, required=True)
  email = db.StringField(unique=True, required=True)
  password = db.StringField(required=True)
  is_admin = db.BooleanField(default=False)
  is_author = db.BooleanField(default=False)


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


# category objeect
class Category(db.Document):
  kategori = db.StringField(required=True)


# modelview object
class MyModelView(ModelView):
  def is_accessible(self):
    return current_user.is_authenticated and current_user.is_admin

  def inaccessible_callback(self, name, **kwargs):
    flash('Login as admin to view admin page')
    return redirect(url_for('login'))


# admin view object
class MyAdminIndexView(AdminIndexView):
  def is_accessible(self):
    return current_user.is_authenticated and current_user.is_admin

  def inaccessible_callback(self, name, **kwargs):
    flash('Login as admin to view this page')
    return redirect(url_for('login'))


# news creation form object
class CreateNewsForm(FlaskForm):
  kategori = list(Category.objects())
  temp = []
  for x in kategori:
    temp.append(x.kategori)
  judul = StringField(label='Judul Berita', validators=[InputRequired()])
  tanggal = DateField(label='Tanggal Pembuatan', format='%Y-%m-%d', default=datetime.utcnow(), validators=[InputRequired()])
  kategori = SelectField(label='Kategori', choices=temp, validators=[InputRequired()])
  tags = StringField(label='Tags (Separate each one by ;)', validators=[InputRequired()])
  rating = IntegerField(label='Rating', default=random.randint(0, 100), validators=[InputRequired()])
  detail = StringField(label='Detail Berita (Separate Each Paragraph by ;)', validators=[InputRequired()])


#  login form object
class LoginForm(FlaskForm):
  username = StringField(label='Username', validators=[InputRequired(), Length(min=4, max=30)])
  password = PasswordField(label='Password', validators=[InputRequired(), Length(max=80)])


# registration form object
class RegistrationForm(FlaskForm):
  username = StringField(label='Username', validators=[InputRequired(), Length(min=4, max=30)])
  email = StringField(label='Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
  password = PasswordField(label='Password', validators=[InputRequired(), Length(min=8, max=80)])


# filter by date form object
class FilterByDateForm(FlaskForm):
  searchText = StringField(label='Filter By Date', validators=[InputRequired()])


# filter by tag form object
class FilterByTagsForm(FlaskForm):
  searchText = StringField(label='Filter By Tags (Separate by ;)', validators=[InputRequired()])


# filter by category form object
class FilterByCategoryForm(FlaskForm):
  searchText = StringField(label='Filter By Category', validators=[InputRequired()])


# filter by author form object
class FilterByAuthorForm(FlaskForm):
  searchText = StringField(label='Filter By Author', validators=[InputRequired()])