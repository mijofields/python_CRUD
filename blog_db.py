from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime
import yaml

app = Flask(__name__)

env = yaml.load(open('db.yaml'))

app.config['SQLALCHEMY_DATABASE_URI'] = env['sqlalchemy_database_uri']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Users(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(25), unique=False, nullable=False)
    lastname = db.Column(db.String(25), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(25), unique=False, nullable=False)
    posts = db.relationship('Posts', backref='users', lazy=True)

class Posts(db.Model):
    postid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    body = db.Column(db.String(1000), unique=False, nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable=False)
   

    def __repr__(self):
        return '<User %r>' % self.username
        

# commands 
# in mysql CREATE DATABASE python_blog_db;
# USE python_blog_db;
# in the py shell
# from blog_db import db
# db.create_all()

# from blog_db import Users
# mike = Users(firstname='Mike', lastname='Fields', email='mike@example.com', username='mikeyf', password='password')
# db.session.add(mike)
# db.session.commit()

# from blog_db import Posts
# post = Posts(title='Test1', body='Body1', userid=1)
# db.session.add(post)
# db.session.commit()