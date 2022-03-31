from flask import Flask, render_template, redirect, session
from functools import wraps
import pymongo

app = Flask(__name__)
app.secret_key = '\x8f\x01}\xd6&\x0eti\x1c\xc5K=\x85\x9a\x8d\xd9'

# database
client = pymongo.MongoClient('localhost', 27017)
db = client.news_blog

# decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  return wrap    

# routes
from user import routes

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')
