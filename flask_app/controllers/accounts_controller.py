from flask import render_template, request, redirect, session
from flask_app.models.login_model import User
from flask_app.models.address_model import Address
from flask_app.models.account_model import Account
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/create')
def new_account():
    return render_template("new_account.html")

@app.route('/create_new_account', methods=["POST"])
def create_account():
    if not User.validate_user(request.form):
        return redirect('/login_page')
    if not Account.validator(request.form):
        return redirect('/create')
    account_data ={
        "account_type" : request.form['account_type'],
        "date_of_birth" : request.form['date_of_birth'],
        "ssn" : request.form['ssn'],
        "annual_income" : request.form['annual_income'],
        "mobile_number" : request.form['mobile_number'],
        "initial_deposit" : request.form['initial_deposit'],
        "address" : request.form['address'],
        "created_at" : request.form['created_at'],
        "updated_at" : request.form['updated_at'],
        "user_id":session['user_id']
    }
    Account.create(account_data)
    return redirect('/user_dashboard')

@app.route('/this_account/<int:id>')
def this_account(id):
    if "user_id" not in session:
        return redirect ("/login_page")
    data = {
        "id":session["user_id"]
    }
    one_user= User.get_one(data)
    one_account=Account.get_by_id({'id':id})
    return render_template("view_one_account.html", one_user=one_user, one_account=one_account)