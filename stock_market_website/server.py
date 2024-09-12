from flask import Flask, render_template, request
import requests
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

app = Flask(__name__)

# MarketStack API details
API_KEY = '6bbc4092ff50b0a5eb35ffcdc72eb7e8'
BASE_URL = 'http://api.marketstack.com/v1/'


# Homepage route
@app.route('/')
def index():
    return render_template('index.html')


# Search stock data
@app.route('/stock', methods=['POST'])
def stock():
    symbol = request.form['symbol']
    url = f'{BASE_URL}eod?access_key={API_KEY}&symbols={symbol}'
    response = requests.get(url)
    data = response.json()

    if 'data' in data:
        stock_data = data['data']

        # Extract dates and closing prices for trend analysis
        stock_dates = [stock['date'] for stock in stock_data]
        stock_close_prices = [stock['close'] for stock in stock_data]

        return render_template(
            'stock.html',
            stock_data=stock_data,
            symbol=symbol,
            stock_dates=stock_dates,
            stock_close_prices=stock_close_prices
        )
    else:
        error_message = 'Stock data not found!'
        return render_template('index.html', error_message=error_message)


# Dashboard route
@app.route('/dashboard')
def dashboard():
    symbol = request.args.get('symbol')
    time_range = request.args.get('range', '7')  # Default to last 7 days

    # Fetch stock data for the specified range
    url = f'{BASE_URL}eod?access_key={API_KEY}&symbols={symbol}&limit={time_range}'
    response = requests.get(url)
    data = response.json()

    if 'data' in data:
        stock_data = data['data']

        # Extract dates, closing prices, and volumes for the selected range
        stock_dates = [stock['date'] for stock in stock_data]
        stock_close_prices = [stock['close'] for stock in stock_data]
        stock_volumes = [stock['volume'] for stock in stock_data]

        # Predict stock prices for the next 5 days
        future_dates, future_prices = predict_stock_prices(stock_dates, stock_close_prices)

        # Combine future_dates and future_prices into a list of tuples
        future_data = list(zip(future_dates, future_prices))

        return render_template(
            'dashboard.html',
            symbol=symbol,
            stock_dates=stock_dates,
            stock_close_prices=stock_close_prices,
            stock_volumes=stock_volumes,
            time_range=time_range,
            future_data=future_data  # Pass the combined data
        )
    else:
        return "Error loading stock data."



# Prediction function
def predict_stock_prices(dates, prices):
    # Convert date strings to a numerical format for model training
    dates = pd.to_datetime(dates).map(lambda date: date.to_julian_date()).values.reshape(-1, 1)
    prices = np.array(prices).reshape(-1, 1)

    # Train the linear regression model
    model = LinearRegression()
    model.fit(dates, prices)

    # Predict the next 5 days
    future_dates = np.array([dates[-1] + i for i in range(1, 6)]).reshape(-1, 1)
    future_prices = model.predict(future_dates)

    return future_dates, future_prices


if __name__ == '__main__':
    app.run(debug=True)
