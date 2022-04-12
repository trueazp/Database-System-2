from mongoengine import *
from datetime import datetime
from api_constants import mongo_password

import json

# connect to db
db_name = "news_express"
password = mongo_password
DB_URI = "mongodb+srv://miaowmere:{}@cluster0.bpg88.mongodb.net/{}?retryWrites=true&w=majority".format(
  password, db_name
)
connect(host=DB_URI)

class News(DynamicDocument):
  judul = StringField(required=True)
  penulis = StringField(required=True)
  tanggal = DateField(required=True)
  kategori = StringField(required=True)
  tags = ListField(field=StringField(), required=True)
  cover = ImageField(required=True)
  rating = IntField(required=True)
  counter = IntField(required=True)
  detail = ListField(field=StringField(), required=True)

  def to_json(self):
    news_dict = {
      "judul": self.judul,
      "penulis": self.penulis,
      "tanggal": self.tanggal,
      "kategori": self.kategori,
      "tags": self.tags,
      "cover": self.cover,
      "rating": self.rating,
      "counter": self.counter,
      "detail": self.detail
    }
    return json.dumps(news_dict)

  meta = {
    "indexes": ["penulis"],
    "ordering": ["-tanggal"]
  }


# creating news 
def create_news():
  news = News (
    judul = "Ini Judul",
    penulis = "Akmal Zuhdy Prasetya",
    tanggal = datetime(2022, 4, 9),
    kategori = 'hiburan',
    tags = ['tag1', 'tag2', 'tag3'],
    rating = 99,
    counter = 0,
    detail = ['detail1', 'detail2', 'detail3']
  )
  news.cover.put(open(file="D:\Kuliah\Semester_6\Sistem Basis Data 2\Group13_DatabaseSystem2_MidProject\static\img\hib1.jpg", mode="rb"), 
  content_type='image/png', filename='hib1.jpg')
  news.save()
  print('done')

# create_news()
news = News.objects()
for x in news:
  print(x.judul, x.penulis, x.tanggal, x.kategori, x.kategori, x.tags, x.cover, x.rating, x.detail)