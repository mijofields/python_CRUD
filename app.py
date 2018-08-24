from flask import Flask, render_template, url_for, redirect
from flask_mysqldb import MySQL
#import flask server
#render_template is template engine
#url_for url generator and load static files
#redirect

app = Flask(__name__)
#instantiate the server

@app.route('/')
def index():
    fruits = ['Banana', 'Tomato', 'Kiwi', 'Mango']
    return render_template('index.html', fruits=fruits)
    # return url_for('index')

@app.route('/about')
def test():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, port=4812)
#debug mode is like nodemon
#port5000 is the default