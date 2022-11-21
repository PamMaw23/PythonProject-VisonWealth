from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import login_model
from flask_app.models import address_model
from flask_app import DATABASE
from flask import flash


class Account:
    def __init__( self , data ):
        self.id = data['id']
        self.account_type = data['account_type']
        self.date_of_birth = data['date_of_birth']
        self.ssn = data['ssn']
        self.annual_income = data['annual_income']
        self.mobile_number = data['mobile_number']
        self.initial_deposit = data['initial_deposit']
        self.address = data['address']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def create(cls, data ):
        query = """
        INSERT INTO users ( account_type , date_of_birth , ssn, annual_income , mobile_number, initial_deposit address, user_id) 
        VALUES ( %(account_type)s, %(date_of_birth)s ,%(ssn)s, %(annual_income)s , %(mobile_number)s,%(initial_deposit)s, %(address)s, %(user_id)s);
        """
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM accounts JOIN users on accounts.user_id=users.id;
        """
        results = connectToMySQL(DATABASE).query_db( query)
        all_accounts = []
        if results:
            for row in results:
                this_account = cls(row)
                user_data = {
                    **row,
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'id':row['users.id']
                }
                this_user = login_model.User(user_data)
                this_account.client = this_user
                all_accounts.append(this_account)
        return all_accounts

    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['account_type']) < 3:
            flash("Account type cannot be blank.")
            is_valid = False
        val=form_data['date_of_birth']
        if val.isdigit() < 1:
            flash("Date of birth cannot be empty.")
            is_valid = False
        if len(form_data['ssn']) < 9:
            flash("Invalid SSN.")
            is_valid = False
        if len(form_data['ssn']) > 9:
            flash("Invalid SSN.")
            is_valid = False
        val=form_data['annual_income']
        if val.isdigit() < 1:
            flash("Annual income cannot be blank.")
            is_valid = False
        val=form_data['initial_deposit']
        if val.isdigit() < 1:
            flash("Initial deposit cannot be blank.")
            is_valid = False
        val=form_data['mobile_number']
        if val.isdigit() < 1:
            flash("Invalid mobile number.")
            is_valid = False
        if len(form_data['address']) < 3:
            flash("Address cannot be blank.")
            is_valid = False
        return is_valid
