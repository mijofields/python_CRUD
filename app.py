from flask import Flask, render_template, url_for, redirect, request, session, flash, g, jsonify
from flask_mysqldb import MySQL
# from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
# from flask_login import LoginManager
# from flask_login import UserMixin
from functools import wraps
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
# login = LoginManager(app)



#configure sqldb
env = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = env['mysql_host']
app.config['MYSQL_USER'] = env['mysql_user']
app.config['MYSQL_PASSWORD'] = env['mysql_password']
app.config['MYSQL_DB'] = env['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#allows table fields to be called like a dict
app.config['SECRET_KEY'] = os.urandom(24)

#sets a random string which is a data key
mysql = MySQL(app)


#user class to facilitate log-in and registration

def login_required(f):
    @wraps(f)
    def wrap (*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Please logni to access your dashboard')
            return redirect(url_for('index'))

    return wrap

# root & index page, showing all blog posts from all authors
@app.route('/', methods= ['GET'])
@app.route('/index', methods=['GET'])
def index():
    cur = mysql.connection.cursor()
    query_result = cur.execute("SELECT posts.title, posts.body, posts.date, users.firstname, users.lastname FROM posts LEFT JOIN users ON posts.userid = users.userid ORDER BY posts.date DESC")
    if query_result > 0:
        posts = cur.fetchall()
    cur.close()
    return render_template('index.html', posts=posts)
    

#login page using hashed password allowing user session
@app.route('/login', methods=['POST'])
def login():

    form = request.form
    username = form['username']
    password = form['password']

    cur = mysql.connection.cursor()
    query_result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
    user_info = cur.fetchone()

    if query_result and password == user_info['password']:
        session['username'] = user_info['username']
        session['userid'] = user_info['userid']
        session['firstname'] = user_info['firstName']
        session['logged_in'] = True

        return redirect('/user/' + username )
        
    elif query_result and password != user_info['password']:
        flash('Incorrect login credentials')
        return redirect(url_for('index'))

    else:
        flash('Incorrect login credentials')
        return redirect(url_for('index'))
        
@app.route('/delete/<postid>', methods=['POST'])
@login_required
def delete(postid):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM posts WHERE postid = %s", [postid])
    mysql.connection.commit()
    cur.close()
    flash('You have deleted your post')
    return render_template('home.html' )
    # return redirect('/user/' + session['username'] )
  
@app.route('/edit/<postid>', methods=['GET','POST'])
@login_required
def editpost(postid):
    
    print('edit working')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts WHERE postid = %s", [postid])
    post = cur.fetchone()
    print(post['title'])
    cur.close()
    return render_template('edit_post.html', post=post)
    # return jsonify({'data': render_template('edit_post.html', post=post)})
    


@app.route('/user/<username>', methods=['GET'])
@login_required
def homepage(username):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts WHERE userid = %s ORDER BY date DESC", [session['userid']])
    posts = cur.fetchall()
    cur.close()
    count = len(posts)
    return render_template('home.html', posts=posts, count=count)


@app.route('/user/<username>', methods=['POST'])
@login_required
def addPost(username):

    form = request.form
    title = form['title']
    body = form['body']
    userid= session['userid']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO posts (title, body, userid) VALUES (%s, %s, %s)", [title, body, userid]), 
    mysql.connection.commit()
    cur.close()
    flash('You have added a post')
    return redirect('/user/' + username )


@app.route('/<username>', methods=['GET'])
def userposts(username):
    cur = mysql.connection.cursor()
    cur.execute("SELECT userid FROM users WHERE username = %s", [username])
    userid = cur.fetchone()
    cur.execute("SELECT posts.title, posts.body, posts.date, users.firstname, users.lastname FROM posts LEFT JOIN users ON posts.userid = users.userid WHERE users.userid = %s ORDER BY posts.date DESC", [userid['userid']])
    posts = cur.fetchall()
    cur.close()
    return render_template('index.html', posts=posts)


@app.route('/logout')
@login_required
def logout():
    session.clear() 
    flash('Thanks for visiting')
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    #e is the error message
    return 'This page was not found you numpty'



if __name__ == '__main__':
    app.run(debug=True, port=4812)
#debug mode is like nodemon
#port5000 is the default