from flask import render_template, request, redirect, session
from flask_app.models.login_model import User
from flask_app.models.address_model import Address
from flask_app.models.account_model import Account
from flask_app import app
import yfinance as yf
import pandas as pd

# data= yf.download(tickers="MSFT", start ="2022-11-16", end="2022-11-17", period="1d", interval="5m")
# for index, row in data.iterrows():
#     cur_date = index.strftime('%m/%d/%Y')
#     cur_time = index.strftime("%H:%M")
#     live_close_price = row['Close']
#     print("Price at" + str(cur_date) +" "+str(cur_time)+"="+str(live_close_price))

# print('Hello Friends')
# print('Welcome')

@app.route('/yahoo_test')
def yahoo_test():
    ticker=["MSFT","GOOGL", "AMZN" ]

    result = []
    for tk in ticker:
        data = yf.Ticker(tk).info
        ticker_data = {
            "symbol": data['symbol'],
            "day_high": data['dayHigh'],
            "day_low": data['dayLow']
        }
        result.append(ticker_data)

    # print(msft.info)
    # print(googl.info)
    # print(amazon.info)
    return result

@app.route('/stock_graph/<stock>')
def stock_graph(stock):
    stock_data = yf.Ticker(stock).history(period="1mo")
    legend = 'Daily Price Tracking'
    values = stock_data["Close"].to_list()
    # Close is the column, stock_data is all the data. Data is a dataframe
    labels = [str(pd.to_datetime(stock_date).date()) for stock_date in stock_data.index]
    #labels is the index. Research list comprehension. str typecasts to a string format
    return legend, values, labels
    
