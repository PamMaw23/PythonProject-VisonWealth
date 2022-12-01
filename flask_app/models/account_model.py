from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import login_model
from flask_app.models import address_model
from flask_app import DATABASE
from flask import flash


class Account:
    def __init__( self , data ):
        self.id = data['id']
        self.currency = data['currency']
        self.transaction_description = data['transaction_description']
        self.account_balance = data['account_balance']
        self.debit = data['debit']
        self.credit = data['credit']
        self.interest_rate = data['interest_rate']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def create(cls, data ):
        query = """
        INSERT INTO users ( currency , transaction_description , account_balance, debit , credit, interest_rate, user_id) 
        VALUES ( %(currency)s, %(transaction_description)s ,%(account_balance)s, %(debit)s , %(credit)s,%(interest_rate)s, %(user_id)s);
        """
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def get_by_id(cls,data):
        query="""
        SELECT * FROM users JOIN investment_accounts on users.id = investment_accounts.user_id WHERE users.id=%(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            account_info = []
            this_user = cls(results[0])
            for row in results:
                user_data = {
                    **row,
                    'id' : row['id'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at']
                }
            this_user = login_model.User(user_data)
            # account_info.planner = this_user
            return account_info
        return False


    # @staticmethod
    # def validator(form_data):
    #     is_valid = True
    #     if len(form_data['currency']) < 3:
    #         flash("Account type cannot be blank.")
    #         is_valid = False
    #     val=form_data['transaction_description']
    #     if val.isdigit() < 1:
    #         flash("Date of birth cannot be empty.")
    #         is_valid = False
    #     if len(form_data['account_balance']) < 9:
    #         flash("Invalid SSN.")
    #         is_valid = False
    #     if len(form_data['account_balance']) > 9:
    #         flash("Invalid SSN.")
    #         is_valid = False
    #     val=form_data['debit']
    #     if val.isdigit() < 1:
    #         flash("Annual income cannot be blank.")
    #         is_valid = False
    #     val=form_data['interest_rate']
    #     if val.isdigit() < 1:
    #         flash("Initial deposit cannot be blank.")
    #         is_valid = False
    #     val=form_data['credit']
    #     if val.isdigit() < 1:
    #         flash("Invalid mobile number.")
    #         is_valid = False
    #     if len(form_data['address']) < 3:
    #         flash("Address cannot be blank.")
    #         is_valid = False
    #     return is_valid
