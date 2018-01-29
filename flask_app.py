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

@app.route('/clubUpload/', methods=['GET', 'POST'])
def clubUpload():
    try:
        return
    except Exception as e:
        return (str(e))

@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    try:
        c, conn = connectionStudent()

        firstname = request.form['firstname']
        lastname = request.form['lastname']
        age = "" + request.form['age']
        email = request.form['email']
        idnumber = "" + request.form['idnumber']
        password = request.form['password']
        confpassword = request.form['confpassword']
        majors = request.form['majors']
        about = request.form['about']
        firstyear = "" + request.form['firstyear']
        school = request.form['school']
        gpa = request.form['gpa']
        volunteer = request.form['volunteer']
        profexp = request.form['profexp']
        certawards = request.form['certawards']
        priors = request.form['priors']
        interests = request.form['interests']
        pronouns = request.form['pronouns']
        race = request.form['race']
        link = "" + request.form['link']

        filename = ''
        resumeFilename = ''

        if 'profilepic' not in request.files:
            pass
            #return redirect(url_for('studentRegister'))

        file = request.files['profilepic']

        if file.filename == '':
            pass
            #return redirect(url_for('studentRegister'))
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        app.config['UPLOAD_FOLDER'] = '/home/aatifjiwani/mysite/BearCrawlApp/static/resumes/'

        if 'resume' not in request.files:
            pass
            #return redirect(url_for('studentRegister'))

        resumeFile = request.files['resume']
        if resumeFile.filename == '':
            pass
            #return redirect(url_for('studentRegister'))
        else:
            resumeFilename = secure_filename(resumeFile.filename)
            resumeFile.save(os.path.join(app.config['UPLOAD_FOLDER'], resumeFilename))

        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        filename = "images/" + filename
        resumeFilename = "resumes/" + resumeFilename

        if password == confpassword:
            c.execute("INSERT INTO users (email, password) VALUES ('%s', '%s')" %
                             (thwart(email), thwart(password)))
            conn.commit()

            c.execute("INSERT INTO profiles (firstname, lastname, age, email, idnumber, majors, about, firstyear, school, gpa, volunteer, profexp, certawards, priors, interests, pronouns, race, link, profilepic, resume) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (thwart(firstname), thwart(lastname), thwart(age), thwart(email), thwart(idnumber), thwart(majors), thwart(about), thwart(firstyear), thwart(school), thwart(gpa), thwart(volunteer), thwart(profexp), thwart(certawards), thwart(priors), thwart(interests), thwart(pronouns), thwart(race), thwart(link), thwart(filename), thwart(resumeFilename)))

            conn.commit()

            c.close()
            conn.close()

            gc.collect()

            session['logged_in'] = True
            session['email'] = email
            session['student'] = True

            return redirect(url_for('profile'))
    except Exception as e:
        return (str(e))

@app.route('/studentRegister/', methods=['GET', 'POST'])
@already_login
def studentRegister():
    return render_template('StudentRegistration.html')


    '''error = ''
    try:
        c, conn = connectionStudent()
        if request.method == "POST":
            data = request.form['about']
            return test(data)
        c.close()
        conn.close()
        gc.collect()

        return render_template('StudentRegistration.html')
    except Exception as e:
        return render_template('StudentRegistration.html')'''

@app.route('/clubRegister/', methods=['GET', 'POST'])
@already_login
def clubRegister():
    return render_template('ClubRegistration.html')

@app.route('/test/')
def test(message):
    return message

@app.route('/about/')
def about():
    return render_template('About.html')

@app.route('/contact/')
def contact():
    return render_template('Contact.html')

@app.route('/profile/')
@login_required
def profile():
    error = ''
    try:
        c, conn = connectionStudent()
        data = c.execute("SELECT * FROM profiles WHERE email = '%s'" % (thwart(session['email'])))
        firstname = c.fetchone()[0]
        
        return render_template('StudentProfile.html', first=firstname )
    except Exception as e:
        return render_template('StudentProfile.html')

@app.route('/clubProfile/')
@login_required
def clubProflile():
    return render_template('ClubProfile.html')

@app.route('/logout/')
@login_required
def logout():
    session.clear()
    #flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('studentLogin'))

if __name__ == "__main__":
    app.run()



