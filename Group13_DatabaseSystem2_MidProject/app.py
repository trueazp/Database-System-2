from bson import ObjectId
from datetime import datetime
from flask_admin import Admin
from flask_login import LoginManager
from flask_paginate import Pagination
from flask_bootstrap import Bootstrap
from api_constants import mongo_password
from flask_mongoengine import MongoEngine
from flask_admin.contrib.mongoengine import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session
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
bootstrap = Bootstrap(app)
db = MongoEngine(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# models
from models import User, News, LoginForm, RegistrationForm, FilterByDateForm

# admin stuff
admin = Admin(app)
admin.add_view(ModelView(User))
admin.add_view(ModelView(News))

# decorators
@login_manager.user_loader
def load_user(userId):
  userId=1
  return User.objects.get(userId=userId)

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

# --------------------------------------------------------- GUEST --------------------------------------------------------- #

# HOMEPAGE / GUEST
@app.route('/home_guest', methods=['POST', 'GET'])
def index_guest():
  form = FilterByDateForm()
  if form.validate_on_submit():
    return redirect('/news_guest_by_date/' + form.searchText.data)
  page = request.args.get('page', 1, type=int)
  news_paginate = News.objects().order_by('-tanggal').paginate(page=page, per_page=3)
  return render_template('guest/guest_index.html', data=news, data_length=len(news), pagination=news_paginate, form=form,
    news_entertainment=news_entertainment, news_entertainment_length=len(news_entertainment), top_entertainment=top_ratings_entertainment,
    news_sport=news_sport, news_sport_length=len(news_sport), top_sport=top_ratings_sport,
    news_political=news_political, news_political_length=len(news_political), top_political=top_ratings_political,
    news_travel=news_travel, news_travel_length=len(news_travel), top_travel=top_ratings_travel,
    news_health=news_health, news_health_length=len(news_health), top_health=top_ratings_health)


# DETAIL PAGE / GUEST
@ app.route('/details_guest/<int:newsId>/', methods=['POST', 'GET'])
def details_guest(newsId):
  form = FilterByDateForm()
  if form.validate_on_submit():
    return redirect('/news_guest_by_date/' + form.searchText.data)
  selected_news = list(News.objects(newsId=newsId))
  return render_template('guest/guest_details.html', data=selected_news, data_length=len(selected_news), form=form, tanggal=form.searchText.data,
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


# LOGIN
@app.route('/login/', methods=['POST', 'GET'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    try:
      user = User.objects.get(username=form.username.data)
    except:
      return render_template('404.html')
    if user:
      if check_password_hash(user.password, form.password.data):
        login_user(user, remember=form.remember.data)
        return redirect(url_for('index'))
      return render_template('404.html')
    return render_template('404.html')
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
@app.route('/test/')
def test():
  news_by_date = News.objects()
  list_news_by_date = list(news_by_date)
  return render_template('guest/test.html', a=news_by_date)

# --------------------------------------------------------- USER --------------------------------------------------------- #

# HOMEPAGE / USER
@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
  form = FilterByDateForm()
  if form.validate_on_submit():
    return redirect('/news_by_date/' + form.searchText.data)
  page = request.args.get('page', 1, type=int)
  news_paginate = News.objects().order_by('-tanggal').paginate(page=page, per_page=3)
  if session['_user_id']:
    username = User.objects.get(id=ObjectId(session['_user_id'])).username
    return render_template('user/index.html', data=news, data_length=len(news), pagination=news_paginate, username=username.split()[0], form=form,
      news_entertainment=news_entertainment, news_entertainment_length=len(news_entertainment), top_entertainment=top_ratings_entertainment,
      news_sport=news_sport, news_sport_length=len(news_sport), top_sport=top_ratings_sport,
      news_political=news_political, news_political_length=len(news_political), top_political=top_ratings_political,
      news_travel=news_travel, news_travel_length=len(news_travel), top_travel=top_ratings_travel,
      news_health=news_health, news_health_length=len(news_health), top_health=top_ratings_health)
    

# DETAIL PAGE / USER
@ app.route('/details/<int:newsId>/', methods=['POST', 'GET'])
@login_required
def details(newsId):
  form = FilterByDateForm()
  if form.validate_on_submit():
    return redirect('/news_by_date/' + form.searchText.data)
  selected_news = list(News.objects(newsId=newsId))
  if session['_user_id']:
    username = User.objects.get(id=ObjectId(session['_user_id'])).username
    return render_template('user/details.html', data=selected_news, data_length=len(selected_news), form=form, username=username.split()[0], tanggal=form.searchText.data,
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


# CREATE NEWS
@app.route('/create_news/')
def create_news():
  # rand = random.randint(50, 100)
  # news = News (
  #   judul = "",
  #   penulis = "",
  #   tanggal = datetime(year, month, day),
  #   kategori = '',
  #   tags = [
  #     ''
  #   ],
  #   rating = rand,
  #   counter = 0,
  #   detail = [
  #     ''
  #   ]
  # )
  # news.cover.put(open(file="file path", mode="rb"), 
  # content_type='image/png', filename='')
  # news.save()
  return redirect('/test')