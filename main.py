#!/usr/bin/env python
# coding=utf-8
from flask import Flask, request,render_template, flash, redirect, url_for,session,logging
from data import Domains,Questions,Answers
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

#configure mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'mpumi'
app.config['MYSQL_PASSWORD'] = 'sabricsql'
app.config['MYSQL_DB'] = 'TESTDB'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#initialize MySQL
mysql = MySQL(app)


Domains = Domains()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/domains')
def domains():
    return render_template('domains.html', domains = Domains)

@app.route('/domain/<string:id>/')
def domain(id):
    cur1 = mysql.connection.cursor()
    cur2 = mysql.connection.cursor()

    result = cur1.execute("SELECT id, question, question_code, answers FROM assessment WHERE DOMAIN = %s",[id] )
    question = cur1.fetchall()

    q = {}
    ans = {}
    for i in question:
        if i['question'] != '':
            q[i['question_code']] = i['question']
            answers = i['answers'].replace('(','')
            answers = answers.replace(')','')
            answers=answers.split(',')
            ans[i['question_code']] = answers
            for x in ans:
                x.encode("utf-8")
            #li_u_removed = [str(i) for i in ans]
    

   
    return render_template('domain.html', question = q, answers =x)


#Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.length(min=1, max=50)])
    username = StringField('Username', [validators.length(min=4, max=50)])
    email = StringField('Email', [validators.length(min=6, max=50)])
    bank = StringField('Bank', [validators.length(min=1, max=50)])
    password = StringField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match') 
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        bank = form.bank.data
        #encrypt password before submitting
        password = sha256_crypt.encrypt(str(form.password.data))

        #create cursor 
        cur = mysql.connection.cursor()

        #execute query
        cur.execute("INSERT INTO users(name,email,username,password,bank) VALUES(%s,%s,%s,%s,%s)",(name,email,username,password,bank))

        #commit to db
        mysql.connection.commit()

        #close connection
        cur.close()

        flash('You are now registered and can login and use the system', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

#User login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            #get stored hash
            data = cur.fetchone()
            password = data['password']

            #compare passwords
            if sha256_crypt.verify(password_candidate, password):
                #passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error) 
            #close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error) 
    return render_template('login.html') 

#Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session: 
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wraps

#Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('logout'))



@app.route('/questions', methods=['GET', 'POST'])
def print_questions():
    selected_assessment = request.args.get('type')
    print(selected_assessment)
    return render_template(questions.html, title='Assessment Questions', questions=questions)

@app.route('/answers', methods=['POST'])
def answers():
    _answers = request.form["inputAnswer"]

@app.route('/', methods=['GET', 'POST'])
def save():
    if request.method == 'POST':
        #fetch form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        username = userDetails['username']
        bank = userDetails['bank']
        domain = userDetails['domain']
        question = userDetails['question']
        requesttype = userDetails['RequestType']

        cur = mysql.connection.cursor()
        cur.execute("""INSERT INTO answers (name, email, username, bank, domain, question, requesttype) VALUES (%s, %s, %s, %s, %s, %s, %s)""", (name, email, username, bank, domain, question, requesttype))
        mysql.connection.commit()
        cur.close()
        return 'Save is successful'
    return render_template('index.html')


    
if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)

