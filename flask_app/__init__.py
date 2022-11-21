from flask import Flask
import yfinance as yf

app = Flask(__name__)
app.secret_key = "secret"
DATABASE ="python_project"

