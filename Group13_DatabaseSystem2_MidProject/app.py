import os
from bson import ObjectId
from datetime import datetime
from flask_admin import Admin
from flask_login import LoginManager
from flask_paginate import Pagination
from flask_bootstrap import Bootstrap
from api_constants import mongo_password
from flask_mongoengine import MongoEngine
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

# init
app = Flask(__name__)
db_name = "news_express"
password = mongo_password
DB_URI = "mongodb+srv://miaowmere:{}@cluster0.bpg88.mongodb.net/{}?retryWrites=true&w=majority".format(
  password, db_name
)
app.config['MONGODB_HOST'] = DB_URI
app.config['SECRET_KEY'] = '\x8f\x01}\xd6&\x0eti\x1c\xc5K=\x85\x9a\x8d\xd9'
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', 'jpeg']
app.config['UPLOAD_PATH'] = 'D:/Kuliah/Semester_6/Sistem Basis Data 2/Group13_DatabaseSystem2_MidProject/static/img/'
bootstrap = Bootstrap(app)
db = MongoEngine(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# models
from models import User, News, Category, MyAdminIndexView, MyModelView, CreateNewsForm, LoginForm, RegistrationForm, FilterByDateForm, FilterByTagsForm, FilterByCategoryForm, FilterByAuthorForm

# admin stuff
admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(MyModelView(User))
admin.add_view(MyModelView(News))
admin.add_view(MyModelView(Category))

# decorators
@login_manager.user_loader
def load_user(userId):
  return User.objects(pk=userId).first()

# get ratings
def get_ratings(data):
  news_type = list(data)
  top = []
  for x in range(len(news_type)):
    top.append(news_type[x].rating)
  top.sort(reverse=True)
  return top

# all news
news = list(News.objects())

# news types
news_entertainment = list(News.objects(kategori='hiburan'))
news_sport = list(News.objects(kategori='olahraga'))
news_political = list(News.objects(kategori='politik'))
news_travel = list(News.objects(kategori='travel'))
news_health = list(News.objects(kategori='kesehatan'))

# top_news
top_ratings_entertainment = get_ratings(news_entertainment)
top_ratings_sport = get_ratings(news_sport)
top_ratings_political = get_ratings(news_political)
top_ratings_travel = get_ratings(news_travel)
top_ratings_health = get_ratings(news_health)

# ---------------------------------------------------------------------------------------------- GUEST ---------------------------------------------------------------------------------------------- #

# HOMEPAGE / GUEST
@app.route('/home_guest', methods=['POST', 'GET'])
def index_guest():
  form_filter_date = FilterByDateForm()
  form_filter_tags = FilterByTagsForm()
  form_filter_category = FilterByCategoryForm()
  form_filter_author = FilterByAuthorForm()

  # if filtered by date
  if form_filter_date.validate_on_submit():
    if request.form['filter_identifier'] == 'filter_by_date':
      return redirect('/news_guest_by_date/' + form_filter_date.searchText.data)
    
  # if filtered by tags
  if form_filter_tags.validate_on_submit():
    if request.form['filter_identifier'] == 'filter_by_tags':
      return redirect('/news_guest_by_tags/' + form_filter_tags.searchText.data)

  # if filtered by category
  if form_filter_category.validate_on_submit():
    if request.form['filter_identifier'] == 'filter_by_category':
      return redirect('/news_guest_by_category/' + form_filter_category.searchText.data.lower())

  # if filtered by author
  if form_filter_author.validate_on_submit():
    if request.form['filter_identifier'] == 'filter_by_author':
      return redirect('/news_guest_by_author/' + form_filter_author.searchText.data)
  
  page = request.args.get('page', 1, type=int)
  news_paginate = News.objects().order_by('-tanggal').paginate(page=page, per_page=3)
  return render_template('guest/guest_index.html', data=news, data_length=len(news), pagination=news_paginate, 
    form_filter_date=form_filter_date, form_filter_tags=form_filter_tags, form_filter_category=form_filter_category, form_filter_author=form_filter_author,
    news_entertainment=news_entertainment, news_entertainment_length=len(news_entertainment), top_entertainment=top_ratings_entertainment,
    news_sport=news_sport, news_sport_length=len(news_sport), top_sport=top_ratings_sport,
    news_political=news_political, news_political_length=len(news_political), top_political=top_ratings_political,
    news_travel=news_travel, news_travel_length=len(news_travel), top_travel=top_ratings_travel,
    news_health=news_health, news_health_length=len(news_health), top_health=top_ratings_health)


# DETAIL PAGE / GUEST
@ app.route('/details_guest/<int:newsId>/', methods=['POST', 'GET'])
def details_guest(newsId):
  form_filter_date = FilterByDateForm()
  form_filter_tags = FilterByTagsForm()
  form_filter_category = FilterByCategoryForm()
  form_filter_author = FilterByAuthorForm()

  # if filtered by date
  if form_filter_date.validate_on_submit():
    if request.form['filter_identifier'] == 'filter_by_date':
      return redirect('/news_guest_by_date/' + form_filter_date.searchText.data)
    
  # if filtered by tags
  if form_filter_tags.validate_on_submit():
    if request.form['filter_identifier'] == 'filter_by_tags':
      return redirect('/news_guest_by_tags/' + form_filter_tags.searchText.data)

  # if filtered by category
  if form_filter_category.validate_on_submit():
    if request.form['filter_identifier'] == 'filter_by_category':
      return redirect('/news_guest_by_category/' + form_filter_category.searchText.data.lower())
  
  # if filtered by author
  if form_filter_author.validate_on_submit():
    if request.form['filter_identifier'] == 'filter_by_author':
      return redirect('/news_guest_by_author/' + form_filter_author.searchText.data)
  
  selected_news = list(News.objects(newsId=newsId))
  return render_template('guest/guest_details.html', data=selected_news, data_length=len(selected_news), 
  form_filter_date=form_filter_date, form_filter_tags=form_filter_tags, form_filter_category=form_filter_category, form_filter_author=form_filter_author,
  news_entertainment=news_entertainment, news_entertainment_length=len(news_entertainment), top_entertainment=top_ratings_entertainment,
  news_sport=news_sport, news_sport_length=len(news_sport), top_sport=top_ratings_sport,
  news_political=news_political, news_political_length=len(news_political), top_political=top_ratings_political,
  news_travel=news_travel, news_travel_length=len(news_travel), top_travel=top_ratings_travel,
  news_health=news_health, news_health_length=len(news_health), top_health=top_ratings_health)


# FILTER NEWS BY DATE / GUEST
@app.route('/news_guest_by_date/<string:tanggal>', methods=['POST', 'GET'])
def filter_news_by_date_guest(tanggal):
  form = FilterByDateForm()
  if form.validate_on_submit():
    return redirect('/news_guest_by_date/' + form.searchText.data)
  page = request.args.get('page', 1, type=int)
  news_paginate = News.objects(tanggal=tanggal).order_by('-tanggal').paginate(page=page, per_page=3)
  return render_template('guest/guest_news_filter_by_date.html', data=news, data_length=len(news), pagination=news_paginate, form=form, tanggal=tanggal,
    news_entertainment=news_entertainment, news_entertainment_length=len(news_entertainment), top_entertainment=top_ratings_entertainment,
    news_sport=news_sport, news_sport_length=len(news_sport), top_sport=top_ratings_sport,
    news_political=news_political, news_political_length=len(news_political), top_political=top_ratings_political,
    news_travel=news_travel, news_travel_length=len(news_travel), top_travel=top_ratings_travel,
    news_health=news_health, news_health_length=len(news_health), top_health=top_ratings_health)


# FILTER NEWS BY TAGS / GUEST
@app.route('/news_guest_by_tags/<string:tags>', methods=['POST', 'GET'])
def filter_news_by_tags_guest(tags):
  form = FilterByTagsForm()
  tags_list = []

  if form.validate_on_submit():
    return redirect('/news_guest_by_tags/' + form.searchText.data)
  
  if ';' in tags:
    splitted = tags.split(';')
    for x in range(len(splitted)):
      tags_list.append(splitted[x])
  else:
    tags_list.append(tags)

  page = request.args.get('page', 1, type=int)
  news_paginate = News.objects(tags__in=tags_list).order_by('-tanggal').paginate(page=page, per_page=3)
  return render_template('guest/guest_news_filter_by_tags.html', data=news, data_length=len(news), pagination=news_paginate, form=form, tags=tags,
    news_entertainment=news_entertainment, news_entertainment_length=len(news_entertainment), top_entertainment=top_ratings_entertainment,
    news_sport=news_sport, news_sport_length=len(news_sport), top_sport=top_ratings_sport,
    news_political=news_political, news_political_length=len(news_political), top_political=top_ratings_political,
    news_travel=news_travel, news_travel_length=len(news_travel), top_travel=top_ratings_travel,
    news_health=news_health, news_health_length=len(news_health), top_health=top_ratings_health)


# FILTER NEWS BY CATEGORY / GUEST
@app.route('/news_guest_by_category/<string:kategori>', methods=['POST', 'GET'])
def filter_news_by_category_guest(kategori):
  form = FilterByCategoryForm()
  if form.validate_on_submit():
    return redirect('/news_guest_by_category/' + form.searchText.data.lower())
  page = request.args.get('page', 1, type=int)
  news_paginate = News.objects(kategori__iexact=kategori).order_by('-tanggal').paginate(page=page, per_page=3)
  return render_template('guest/guest_news_filter_by_category.html', data=news, data_length=len(news), pagination=news_paginate, form=form, kategori=kategori,
    news_entertainment=news_entertainment, news_entertainment_length=len(news_entertainment), top_entertainment=top_ratings_entertainment,
    news_sport=news_sport, news_sport_length=len(news_sport), top_sport=top_ratings_sport,
    news_political=news_political, news_political_length=len(news_political), top_political=top_ratings_political,
    news_travel=news_travel, news_travel_length=len(news_travel), top_travel=top_ratings_travel,
    news_health=news_health, news_health_length=len(news_health), top_health=top_ratings_health)


# FILTER NEWS BY AUTHOR / GUEST
@app.route('/news_guest_by_author/<string:penulis>', methods=['POST', 'GET'])
def filter_news_by_author_guest(penulis):
  form = FilterByAuthorForm()
  if form.validate_on_submit():
    return redirect('/news_guest_by_author/' + form.searchText.data)
  page = request.args.get('page', 1, type=int)
  news_paginate = News.objects(penulis__icontains=penulis).order_by('-tanggal').paginate(page=page, per_page=3)
  return render_template('guest/guest_news_filter_by_author.html', data=news, data_length=len(news), pagination=news_paginate, form=form, penulis=penulis,
    news_entertainment=news_entertainment, news_entertainment_length=len(news_entertainment), top_entertainment=top_ratings_entertainment,
    news_sport=news_sport, news_sport_length=len(news_sport), top_sport=top_ratings_sport,
    news_political=news_political, news_political_length=len(news_political), top_political=top_ratings_political,
    news_travel=news_travel, news_travel_length=len(news_travel), top_travel=top_ratings_travel,
    news_health=news_health, news_health_length=len(news_health), top_health=top_ratings_health)


# LOGIN
@app.route('/login/', methods=['POST', 'GET'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    try:
      user = User.objects.get(username=form.username.data)
    except:
      flash('Invalid Username', 'error')
      return redirect(url_for('login'))
    if user:
      if check_password_hash(user.password, form.password.data):
        login_user(user)
        return redirect(url_for('index'))
      flash('Invalid Password') 
      return redirect(url_for('login'))
    flash('Invalid Username')
    return redirect(url_for('login'))
  
  return render_template('guest/login.html', form=form)


# REGISTER
@app.route('/register/', methods=['POST', 'GET'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password = generate_password_hash(form.password.data, method='sha256')
    new_user = User(
      username = form.username.data,
      email = form.email.data,
      password = hashed_password
    )
    new_user.save()
    return redirect(url_for('login'))
  return render_template('guest/register.html', form=form)


# TESTING
@app.route('/test/', methods=['POST', 'GET'])
def test():
  # temp = current_user
  temp = User.objects.get(id=ObjectId(session['_user_id']))
  return render_template('guest/test.html', a=temp.is_author, b=temp.username)

# ---------------------------------------------------------------------------------------------- USER ---------------------------------------------------------------------------------------------- #

# HOMEPAGE / USER
@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
  form_filter_date = FilterByDateForm()
  form_filter_tags = FilterByTagsForm()
  form_filter_category = FilterByCategoryForm()
  form_filter_author = FilterByAuthorForm()

  # if filtered by date
  if form_filter_date.validate_on_submit():
    if request.form['filter_identifier'] == 'filter_by_date':
      return redirect('/news_by_date/' + form_filter_date.searchText.data)
  
  # if filtered by tags
  if form_filter_tags.validate_on_submit():
    if request.form['filter_identifier'] == 'filter_by_tags':
      return redirect('/news_by_tags/' + form_filter_date.searchText.data)

  # if filtered by category
  if form_filter_category.validate_on_submit():
    if request.form['filter_identifier'] == 'filter_by_category':
      return redirect('/news_by_category/' + form_filter_category.searchText.data)

  # if filtered by author
  if form_filter_author.validate_on_submit():
    if request.form['filter_identifier'] == 'filter_by_author':
      return redirect('/news_by_author/' + form_filter_author.searchText.data)

  page = request.args.get('page', 1, type=int)
  news_paginate = News.objects().order_by('-tanggal').paginate(page=page, per_page=3)
  if session['_user_id']:
    username = User.objects.get(id=ObjectId(session['_user_id'])).username
    return render_template('user/index.html', data=news, data_length=len(news), pagination=news_paginate, username=username.split()[0], 
      form_filter_date=form_filter_date, form_filter_tags=form_filter_tags, form_filter_category=form_filter_category, form_filter_author=form_filter_author,
      news_entertainment=news_entertainment, news_entertainment_length=len(news_entertainment), top_entertainment=top_ratings_entertainment,
      news_sport=news_sport, news_sport_length=len(news_sport), top_sport=top_ratings_sport,
      news_political=news_political, news_political_length=len(news_political), top_political=top_ratings_political,
      news_travel=news_travel, news_travel_length=len(news_travel), top_travel=top_ratings_travel,
      news_health=news_health, news_health_length=len(news_health), top_health=top_ratings_health)
    

# DETAIL PAGE / USER
@ app.route('/details/<int:newsId>/', methods=['POST', 'GET'])
@login_required
def details(newsId):
  form_filter_date = FilterByDateForm()
  form_filter_tags = FilterByTagsForm()
  form_filter_category = FilterByCategoryForm()
  form_filter_author = FilterByAuthorForm()

  # if filtered by date
  if form_filter_date.validate_on_submit():
    if request.form['filter_identifier'] == 'filter_by_date':
      return redirect('/news_by_date/' + form_filter_date.searchText.data)
  
  # if filtered by tags
  if form_filter_tags.validate_on_submit():
    if request.form['filter_identifier'] == 'filter_by_tags':
      return redirect('/news_by_tags/' + form_filter_date.searchText.data)

  # if filtered by category
  if form_filter_category.validate_on_submit():
    if request.form['filter_identifier'] == 'filter_by_category':
      return redirect('/news_by_category/' + form_filter_category.searchText.data)

  # if filtered by author
  if form_filter_author.validate_on_submit():
    if request.form['filter_identifier'] == 'filter_by_author':
      return redirect('/news_by_author/' + form_filter_author.searchText.data)

  selected_news = list(News.objects(newsId=newsId))
  if session['_user_id']:
    username = User.objects.get(id=ObjectId(session['_user_id'])).username
    return render_template('user/details.html', data=selected_news, data_length=len(selected_news), username=username.split()[0],
    form_filter_date=form_filter_date, form_filter_tags=form_filter_tags, form_filter_category=form_filter_category, form_filter_author=form_filter_author,
    news_entertainment=news_entertainment, news_entertainment_length=len(news_entertainment), top_entertainment=top_ratings_entertainment,
    news_sport=news_sport, news_sport_length=len(news_sport), top_sport=top_ratings_sport,
    news_political=news_political, news_political_length=len(news_political), top_political=top_ratings_political,
    news_travel=news_travel, news_travel_length=len(news_travel), top_travel=top_ratings_travel,
    news_health=news_health, news_health_length=len(news_health), top_health=top_ratings_health)


# LOG OUT
@app.route('/logout/')
@login_required
def logout():
  logout_user()
  return redirect(url_for('index_guest'))


# FILTER NEWS BY DATE / USER
@app.route('/news_by_date/<string:tanggal>', methods=['POST', 'GET'])
@login_required
def filter_news_by_date(tanggal):
  form = FilterByDateForm()
  if form.validate_on_submit():
    return redirect('/news_by_date/' + form.searchText.data)
  page = request.args.get('page', 1, type=int)
  news_paginate = News.objects(tanggal=tanggal).order_by('-tanggal').paginate(page=page, per_page=3)
  if session['_user_id']:
    username = User.objects.get(id=ObjectId(session['_user_id'])).username
    return render_template('user/news_filter_by_date.html', data=news, data_length=len(news), pagination=news_paginate, username=username.split()[0], form=form, tanggal=tanggal,
      news_entertainment=news_entertainment, news_entertainment_length=len(news_entertainment), top_entertainment=top_ratings_entertainment,
      news_sport=news_sport, news_sport_length=len(news_sport), top_sport=top_ratings_sport,
      news_political=news_political, news_political_length=len(news_political), top_political=top_ratings_political,
      news_travel=news_travel, news_travel_length=len(news_travel), top_travel=top_ratings_travel,
      news_health=news_health, news_health_length=len(news_health), top_health=top_ratings_health)


# FILTER NEWS BY TAGS / USER
@app.route('/news_by_tags/<string:tags>', methods=['POST', 'GET'])
def filter_news_by_tags(tags):
  form = FilterByTagsForm()
  tags_list = []

  if form.validate_on_submit():
    return redirect('/news_by_tags/' + form.searchText.data)
  
  if ';' in tags:
    splitted = tags.split(';')
    for x in range(len(splitted)):
      tags_list.append(splitted[x])
  else:
    tags_list.append(tags)

  page = request.args.get('page', 1, type=int)
  news_paginate = News.objects(tags__in=tags_list).order_by('-tanggal').paginate(page=page, per_page=3)
  if session['_user_id']:
    username = User.objects.get(id=ObjectId(session['_user_id'])).username
    return render_template('user/news_filter_by_tags.html', data=news, data_length=len(news), pagination=news_paginate, username=username.split()[0], form=form, tags=tags,
      news_entertainment=news_entertainment, news_entertainment_length=len(news_entertainment), top_entertainment=top_ratings_entertainment,
      news_sport=news_sport, news_sport_length=len(news_sport), top_sport=top_ratings_sport,
      news_political=news_political, news_political_length=len(news_political), top_political=top_ratings_political,
      news_travel=news_travel, news_travel_length=len(news_travel), top_travel=top_ratings_travel,
      news_health=news_health, news_health_length=len(news_health), top_health=top_ratings_health)


# FILTER NEWS BY CATEGORY / USER
@app.route('/news_by_category/<string:kategori>', methods=['POST', 'GET'])
def filter_news_by_category(kategori):
  form = FilterByCategoryForm()
  if form.validate_on_submit():
    return redirect('/news_by_category/' + form.searchText.data.lower())
  page = request.args.get('page', 1, type=int)
  news_paginate = News.objects(kategori__iexact=kategori).order_by('-tanggal').paginate(page=page, per_page=3)
  if session['_user_id']:
    username = User.objects.get(id=ObjectId(session['_user_id'])).username
  return render_template('user/news_filter_by_category.html', data=news, data_length=len(news), pagination=news_paginate, username=username.split()[0], form=form, kategori=kategori,
    news_entertainment=news_entertainment, news_entertainment_length=len(news_entertainment), top_entertainment=top_ratings_entertainment,
    news_sport=news_sport, news_sport_length=len(news_sport), top_sport=top_ratings_sport,
    news_political=news_political, news_political_length=len(news_political), top_political=top_ratings_political,
    news_travel=news_travel, news_travel_length=len(news_travel), top_travel=top_ratings_travel,
    news_health=news_health, news_health_length=len(news_health), top_health=top_ratings_health)


# FILTER NEWS BY AUTHOR / USER
@app.route('/news_by_author/<string:penulis>', methods=['POST', 'GET'])
def filter_news_by_author(penulis):
  form = FilterByAuthorForm()
  if form.validate_on_submit():
    return redirect('/news_by_author/' + form.searchText.data)
  page = request.args.get('page', 1, type=int)
  news_paginate = News.objects(penulis__icontains=penulis).order_by('-tanggal').paginate(page=page, per_page=3)
  if session['_user_id']:
    username = User.objects.get(id=ObjectId(session['_user_id'])).username
  return render_template('user/news_filter_by_author.html', data=news, data_length=len(news), pagination=news_paginate, username=username.split()[0], form=form, penulis=penulis,
    news_entertainment=news_entertainment, news_entertainment_length=len(news_entertainment), top_entertainment=top_ratings_entertainment,
    news_sport=news_sport, news_sport_length=len(news_sport), top_sport=top_ratings_sport,
    news_political=news_political, news_political_length=len(news_political), top_political=top_ratings_political,
    news_travel=news_travel, news_travel_length=len(news_travel), top_travel=top_ratings_travel,
    news_health=news_health, news_health_length=len(news_health), top_health=top_ratings_health)


# CREATE NEWS
@app.route('/create_news/', methods=['POST', 'GET'])
@login_required
def create_news():
  form = CreateNewsForm()
  username = User.objects.get(id=ObjectId(session['_user_id'])).username
  if User.objects.get(id=ObjectId(session['_user_id'])).is_author:
    if form.validate_on_submit():
      news = News(
        judul=form.judul.data, penulis=username, tanggal=form.tanggal.data, 
        kategori=form.kategori.data.lower(), rating=form.rating.data, counter=0,
        tags=form.tags.data.split(';'), detail=form.detail.data.split(';')
      ) 
      file = request.files['cover']
      filename = secure_filename(file.filename)
      if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
          flash('File Extension is Invalid (only .png, .jpg, .jpeg is valid)', 'error')
          return redirect('/create_news/')
        file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
      news.cover.put(open(file=os.path.join(app.config['UPLOAD_PATH'], filename), mode='rb'), content_type='image/png', filename=filename)
      news.save()
      flash('New News Has Been Created', 'info')
      return render_template('user/create_news.html', form=form, username=username)
  else:
    flash('You are not registered as an author', 'error')
    return redirect('/')
  return render_template('user/create_news.html', form=form, username=username.split()[0])


# ADMIN PAGE
@app.route('/admin/')
@login_required
def admin():
  return render_template('admin/index.html')