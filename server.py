from flask_app.controllers import login_controller
from flask_app.controllers import accounts_controller
from flask_app.controllers import yahoo_finance
from flask_app import app
import yfinance as yf


            
if __name__ == "__main__":
    app.run(debug=True)


