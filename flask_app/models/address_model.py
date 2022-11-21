from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import account_model
from flask_app.models import login_model
from flask_app import DATABASE
from flask import flash


class Address:
    def __init__( self , data ):
        self.id = data['id']
        self.street = data['street']
        self.city = data['city']
        self.state = data['state']
        self.zip_code = data['zip_code']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.account_id = data['account_id']