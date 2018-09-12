from flask import Flask, render_template, url_for, redirect, request, session, flash, g, jsonify
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
from functools import wraps
import yaml
import os
import sys
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import Form, BooleanField, StringField, PasswordField, TextAreaField, validators


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

#data validation classes:

class RegisterForm(Form):
    firstname = StringField('Firstname', [validators.Length(min=1, max=25)])
    lastname = StringField('Lastname', [validators.Length(min=1, max=25)])
    username = StringField('Username', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=100)])
    password = PasswordField('Password', [validators.Length(min=4, max=10)])

class ArticleForm(Form):
    title = StringField('Title', [validators.Length(max=100)])
    body = StringField('Body', [validators.Length(max=1000)])

#login required decorator
def login_required(f):
    @wraps(f)
    def wrap (*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Please log-ni to access your dashboard')
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
    else:
        flash('There have been no posts, yet.')
        return render_template('index.html')
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST' and form.validate():
        firstname = form.firstname.data
        lastname = form.lastname.data
        username = form.username.data
        email = form.email.data
        passwordActual = form.passwordActual.data
        passwordHash = generate_password_hash(passwordActual)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (firstname, lastname, username, email, passwordActual, passwordHash) VALUES (%s, %s, %s, %s, %s, %s)", [firstname, lastname, username, email, passwordActual, passwordHash])
        mysql.connection.commit()
        cur.close()
        flash('You are registered, you can now log-ni using your credentials!')
        return redirect(url_for('index'))

    else:
        flash('Something went wrong with your registration, please try again.\n fistname < 50 characters. \n lastname < 50 characters. \n username < 50 characters. \n email > 4 and < 100 characters. \n password > 4 and < 10 characters.')
        return redirect(url_for('index'))

#login page using hashed password allowing user session
@app.route('/login', methods=['POST'])
def login():

    form = request.form
    username = form['username']
    password = form['password']

    cur = mysql.connection.cursor()
    query_result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
    user_info = cur.fetchone()

    if query_result and check_password_hash(user_info['passwordHash'], password):
        session['username'] = user_info['username']
        session['userid'] = user_info['userid']
        session['firstname'] = user_info['firstname']
        session['logged_in'] = True
        flash('Welcome back ' + session['firstname'] + '.')
        return redirect('/user/' + username )
        
    elif query_result and not check_password_hash(user_info['passwordHash'], password):
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
    flash('You have deleted a post')
    return redirect('/user/' + session['username'] )
  
@app.route('/edit/<postid>', methods=['GET','POST'])
@login_required
def editpost(postid):

    form = ArticleForm(request.form)

    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        cur = mysql.connection.cursor()
        cur.execute("UPDATE posts SET title=%s, body=%s WHERE postid=%s", [title, body, postid])
        mysql.connection.commit()
        cur.close()
        flash('You have updated a post')
        return redirect('/user/' + session['username'] )

    elif request.method == 'POST' and not form.validate():
        flash('Something went wrong with your post. Please keep title to less than 100 characters and body to less than 1000 characters.')
        return redirect('/user/' + session['username'] )

    elif request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM posts WHERE postid = %s", [postid])
        post = cur.fetchone()
        cur.close()
        return render_template('edit_post.html', post=post)

    else:
        flash('That was an invalid request')
        return redirect('/user/' + session['username'] )

@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def homepage(username):
    form = ArticleForm(request.form)

    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM posts WHERE userid = %s ORDER BY date DESC", [session['userid']])
        posts = cur.fetchall()
        cur.close()
        count = len(posts)
        return render_template('home.html', posts=posts, count=count)

    elif request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO posts (title, body, userid) VALUES (%s, %s, %s)", [title, body, session['userid']]), 
        mysql.connection.commit()
        cur.close()
        flash('You have added a post')
        return redirect('/user/' + username )

    elif request.method == 'POST' and not form.validate():
        flash('Please make sure the title is less than 100 characters and the body less than 1000 characters.')
        return redirect('/user/' + username )

    else: 
        flash('This http verb request is not currently supported')
        return redirect('/user/' + username )



@app.route('/<username>', methods=['GET'])
def userposts(username):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT userid FROM users WHERE username = %s", [username])
        userid = cur.fetchone()
        cur.execute("SELECT posts.title, posts.body, posts.date, users.firstname, users.lastname FROM posts LEFT JOIN users ON posts.userid = users.userid WHERE users.userid = %s ORDER BY posts.date DESC", [userid['userid']])
        posts = cur.fetchall()
        cur.close()
        flash('The posts of ' + username)
        return render_template('index.html', posts=posts)
    except:
        flash('The username ' + username + ' does not exist, sorry.')
        return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
    session.clear() 
    flash('Thanks for visiting')
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    #e is the error message
    return '404: This page was not found.'



if __name__ == '__main__':
    app.run(debug=True, port=4812)
#debug mode is like nodemon
#port5000 is the default