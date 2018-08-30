from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:5qlp5word@localhost/python_blog_db'
db = SQLAlchemy(app)


class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(25), unique=False, nullable=False)
    lastname = db.Column(db.String(25), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(25), unique=False, nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)

class Post(db.Model):
    postid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False, nullable=False)
    body = db.Column(db.String(1000), unique=False, nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
   

    def __repr__(self):