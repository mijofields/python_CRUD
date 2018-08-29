from flask import Flask, render_template, url_for, redirect, request, session
from flask_mysqldb import MySQL
from flask import json
from flask_bootstrap import Bootstrap
import yaml
import os
from werkzeug.security import generate_password_hash, check_password_hash

#import flask server
#render_template is template engine
#url_for url generator and load static files
#redirect

app = Flask(__name__)
#instantiate the server
Bootstrap(app)


#configure sqldb
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#allows table fields to be called like a dict
app.config['SECRET_KEY'] = os.urandom(24)
#sets a random string which is a data key
mysql = MySQL(app)

# index page, showing all blog posts from all authors
@app.route('/', methods= ['GET'])
def index():
    cur = mysql.connection.cursor()
    query_result = cur.execute("SELECT posts.title, posts.body, posts.date, posts.postid, users.firstname, users.lastname FROM posts LEFT JOIN users ON posts.author = users.userid;")
    if query_result > 0:
        posts = cur.fetchall()
    return render_template('index.html', posts=posts)
    
    # return url_for('index')
    # session['username'] = employees[0]['name']

    # cur.execute("INSERT INTO user VALUES (%s)", ['Bains'])
    # mysql.connection.commit()

    # if request.method =='POST':
    #     # return 'Succesfully Registered'
    #     return request.form['Password']

#login page using hashed password allowing user session
@app.route('/login', methods=['POST'])
def login():

    form = request.form
    username = form['username']
    password = form['password']
    loginObj = {"username": username, "password": password}
    print(loginObj)
    print(username)
    print(password)

    cur = mysql.connection.cursor()
    query_result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
    user_info = cur.fetchone()

    if query_result and password == user_info['password']:
        session['username'] = user_info['username']
        session['userid'] = user_info['userid']
        return redirect('/user/' + username )
        
    elif query_result and password != user_info['password']:
        return str('wrong password you cunt, stop hacking')
    else:
        return str('you cunt, sign up')

    # return render_template('index.html', posts=posts)
    #some code here to check username password and return to homepage

    # return username

    # redirect(url_for('index') + '#login_modal')
    # return render_template('login.html')

#once login complete allow author to edit posts or create new ones
@app.route('/user/<username>', methods=['GET', 'POST'])
def homepage(username):
    cur = mysql.connection.cursor()
    query_result = cur.execute("SELECT * FROM posts WHERE author = %s", [session['userid']])
    posts = cur.fetchall()
    return render_template('home.html', posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    #e is the error message
    return 'This page was not found you numpty'



if __name__ == '__main__':
    app.run(debug=True, port=4812)
#debug mode is like nodemon
#port5000 is the default