from flask import Flask, flash, redirect, render_template, \
     request, url_for, session
    
from werkzeug.utils import secure_filename

import gc

import os

from MySQLdb import escape_string as thwart

from dbstudent import connectionStudent
from dbclub import connectionClub

from functools import wraps
    
app = Flask(__name__)
app.secret_key = 'some_secret'

UPLOAD_FOLDER = '/home/aatifjiwani/mysite/BearCrawlApp/static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            #flash("You need to login first")
            return redirect(url_for('studentLogin'))
    return wrap

def already_login(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return redirect(url_for('profile'))
        else:
            return f(*args, **kwargs)
    return wrap

@app.route('/')
def index():
    c, conn = connectionStudent()
    return render_template("index.html")

@app.route('/studentLogin/', methods=['GET', 'POST'])
@already_login
def studentLogin():
    error = ''
    try:
        c, conn = connectionStudent()
        if request.method == "POST":
            data = c.execute("SELECT * FROM users WHERE email = '%s'" % (thwart(request.form['email'])))
            data = c.fetchone()[1]
            if data == thwart(request.form['password']):
                session['logged_in'] = True
                session['email'] = thwart(request.form['email'])
                session['student'] = True
                return redirect(url_for('profile'))
            else:
                return render_template('StudentLogin.html')


        c.close()
        conn.close()
        gc.collect()
        return render_template('StudentLogin.html')

    except Exception as e:
        #flash(e)
        error = "Invalid credentials, try again."
        return render_template('StudentLogin.html')


@app.route('/clubLogin/', methods=['GET', 'POST'])
@already_login
def clubLogin():
    error = ''
    try:
        c, conn = connectionClub()
        if request.method == "POST":
            data = c.execute("SELECT * FROM clubs WHERE email = '%s'" % (thwart(request.form['email'])))
            data = c.fetchone()[1]
            if data == thwart(request.form['password']):
                session['logged_in'] = True
                session['email'] = thwart(request.form['email'])
                session['club'] = True
                return redirect(url_for('clubProfile'))
            else:
                return render_template('ClubLogin.html')


        c.close()
        conn.close()
        gc.collect()
        return render_template('ClubLogin.html')

    except Exception as e:
        #flash(e)
        error = "Invalid credentials, try again."
        return render_template('ClubLogin.html')

if __name__ == "__main__":
    app.run()