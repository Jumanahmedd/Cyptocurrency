#importing libraries
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from functools import wraps

#importing the other files to use be able to use the functions
from sqlhelpers import *
from form import *

#library to get the timestamp
import time

#initialize our app
app = Flask(__name__)

#configure all the settings for the sql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'#password created in MySQL application
app.config['MYSQL_DB'] = 'crypto'#name of the database we created in the terminal
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

#wrap function to see if the user is logged in or not
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized access, please login first.", "danger")
            return redirect(url_for('login'))
    return wrap

#
def login_user(username):
    users = Table("users", "name", "email", "username", "password")
    user = users.getone("username", username)

    session['logged_in'] = True
    session['username'] = username
    session['name'] = user.get('name')
    session['email'] = user.get('email')

#signup page
@app.route("/registration",methods = ['GET','POST'])
def registration():
    form = Registeration_form(request.form)
    users = Table("users","name","email","username","password")

    #if the button was pressed in the registration page
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        name = form.name.data

        if isnewuser(username):#if its a new user the data will be inserted in the table
            password = sha256_crypt.encrypt(form.password.data)
            users.insert(name,email,username,password)
            login_user(username)
            return redirect(url_for('dashboard'))
        else:#if not a message will tell the user that this user already exists and to redirects them to the reistration form
            flash('user already exists','danger')
            return redirect(url_for('registration'))
    return render_template('registration.html', form=form)

#login page
@app.route("/login", methods = ['GET','POST'])
def login():
    #if the button in the login page was pressed
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = Table("users","name","email","username","password")
        user = users.getone("username",username)
        real_password = user.get('password')

        if real_password is None:
            flash("Username is not found","danger")
            return redirect(url_for('login'))
        else:
            if sha256_crypt.verify(password, real_password):
                login_user(username)
                flash('You have logged in successfully','success')
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid Password" , 'danger')
                return redirect(url_for('login'))

    return render_template('login.html')

@app.route("/transaction", methods = ['GET', 'POST'])
@is_logged_in
def transaction():
    form = sendMoney_form(request.form)
    balance = get_balance(session.get('username'))

    if request.method == 'POST':
        try:
            send_money(session.get('username'), form.username.data, form.amount.data)
            flash("Transaction was successfully!", "success")
        except Exception as e:
            flash(str(e), 'danger')

        return redirect(url_for('transaction'))

    return render_template('transaction.html', balance=balance, form=form, page='transaction')

@app.route("/buy", methods = ['GET','POST'])
@is_logged_in
def buy():
    form = buying_form(request.form)
    balance = get_balance(session.get('username'))

    if request.method == 'POST':
        try:
            send_money("BANK", session.get('username'), form.amount.data)
            flash("Your purchase was successful!","success")
        except Exception as e:
            flash(str(e), 'danger')

        return redirect(url_for('dashboard'))
    return render_template('buy.html', balance=balance, form=form, page='buy')

@app.route("/logout")
@is_logged_in
def logout():
    session.clear()
    flash("Logged out successfully!","success")
    return redirect(url_for('login'))
    #return render_template('logout.html')

#main page
@app.route("/Dashboard")
@is_logged_in
def dashboard():
    balance = 150#get_balance(session.get('username'))
    blockchain = get_blockchain().chain
    current_time = time.strftime("%I:%M %p")
    return render_template('Dashboard.html',balance=balance, session=session, current_time=current_time, blockchain=blockchain, page='Dahsboard')

@app.route("/")#this will be the main page (the first page to be displayed)
@app.route("/index")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug = True)
