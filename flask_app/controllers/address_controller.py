from flask import render_template, request, redirect, session
from flask_app.models.login_model import User
from flask_app.models.address_model import Address
from flask_app.models.account_model import Account
from flask_app.controllers.yahoo_finance import yahoo_test, stock_graph
from flask_app import app
from flask import flash
import yfinance as yf
import pandas as pd
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def sign_up():
    if not User.validate_user(request.form):
        return redirect('/login_page')
    pw_hash=bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form, 
        "password": pw_hash
    }
    session["user_id"]=User.create(data)
    return redirect("/user_dashboard")

@app.route('/login_page')
def display_login():
    return render_template("login.html")

@app.route('/login', methods=["POST"])
def login():
    data = {
        "email": request.form['email']
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password", "log")
        return redirect("/login_page")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", "log")
        return redirect("/login_page")
    session['user_id'] = user_in_db.id
    return redirect("/user_dashboard")

@app.route("/user_dashboard")
def show_user(stock=None):
    if "user_id" not in session:
        return redirect ("/login_page")
    data = {
        "id":session["user_id"]
    }
    one_user= User.get_one(data)
    all_accounts = Account.get_all()
    stock_data= yahoo_test()
    # legend, values, labels = stock_graph(stock_data[0]["symbol"])
    #the default graph is the first element in the stock_data dictionary
    stock_data = yf.Ticker(stock).history(period="1mo")
    legend = 'Daily Price Tracking'
    values = stock_data["Close"].to_list()
    # Close is the column, stock_data is all the data. Data is a dataframe
    labels = [str(pd.to_datetime(stock_date).date()) for stock_date in stock_data.index]
    return render_template("user_dashboard.html", one_user=one_user, all_accounts=all_accounts, stock_data=stock_data, values=values, labels=labels, legend=legend)

@app.route('/user_logout')
def logout():
    session.clear()
    return render_template("index.html")


