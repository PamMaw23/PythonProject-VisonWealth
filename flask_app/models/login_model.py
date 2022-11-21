from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import account_model
from flask_app.models import address_model
from flask_app import DATABASE
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def create(cls, data ):
        query = """
        INSERT INTO users ( first_name , last_name , email , password) 
        VALUES ( %(first_name)s, %(last_name)s , %(email)s , %(password)s);
        """
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def get_by_email(cls,data):
        query ="SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result)<1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_by_id(cls,data):
        query="""
        SELECT * FROM users JOIN accounts on users.id = accounts.user_id WHERE users.id=%(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            account_list = []
            this_user = cls(results[0])
            for row in results:
                recipe_data = {
                    **row,
                    'id' : row['id'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at']
                }
                this_account_instance = account_model.Recipe(recipe_data)
                account_list.append(this_account_instance)
            this_user.accounts=account_list
        return False
        
    @staticmethod
    def validate_user(data:dict):
        is_valid = True
        if len(data['first_name'])<2:
            flash("First name must be at least 2 characters.", "reg")
            is_valid=False
        if len(data['last_name'])<2:
            flash("Last name must be at least 2 characters.", "reg")
            is_valid=False
        if len(data['email'])<10:
            flash("Email must be at least 10 characters.", "reg")
            is_valid=False
        elif not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", "reg")
            is_valid = False
        else:
            pass_data={
                'email': data['email']
            }
            potential_user = User.get_by_email(pass_data)
            if potential_user:
                flash("Email is already registered", "reg")
                is_valid = False
        if len(data['password'])<1:
            is_valid=False
            flash("Password required.", "reg")
        elif not (data['password']) == (data['confirm_pw']):
            flash("Passwords must match.", 'reg')
            is_valid=False
        return is_valid
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False