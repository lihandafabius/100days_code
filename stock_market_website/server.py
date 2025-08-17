from flask import Flask, render_template, request, send_file
import requests
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import base64
import io
import plotly.graph_objects as go

app = Flask(__name__)

# MarketStack API details
API_KEY = ''
BASE_URL = 'http://api.marketstack.com/v1/'

# Homepage route
@app.route('/')
def index():
    return render_template('index.html')


# Search stock data
@app.route('/stock', methods=['GET', 'POST'])
def stock():
    if request.method == 'POST':
        symbol = request.form['symbol']
    else:
        symbol = request.args.get('symbol')  # For GET request

    if symbol:
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

    return "Error: No stock symbol provided."


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

        # Plot visualizations (static images)
        plot_closing_price(stock_dates, stock_close_prices)
        plot_volume(stock_dates, stock_volumes)
        plot_boxplot(stock_close_prices)
        plot_predicted_stock(stock_dates, stock_close_prices, future_dates, future_prices)

        return render_template(
            'dashboard.html',
            symbol=symbol,
            time_range=time_range,
            future_data=list(zip(future_dates, future_prices))
        )
    else:
        return "Error loading stock data."



@app.route('/compare', methods=['POST'])
def compare_stocks():
    symbol1 = request.form['symbol1']
    symbol2 = request.form['symbol2']

    if symbol1 and symbol2:
        url1 = f'{BASE_URL}eod?access_key={API_KEY}&symbols={symbol1}'
        url2 = f'{BASE_URL}eod?access_key={API_KEY}&symbols={symbol2}'

        response1 = requests.get(url1)
        response2 = requests.get(url2)

        data1 = response1.json()
        data2 = response2.json()

        if 'data' in data1 and 'data' in data2:
            stock_data1 = data1['data']
            stock_data2 = data2['data']

            # Extract dates and closing prices
            dates1 = [stock['date'] for stock in stock_data1]
            prices1 = [stock['close'] for stock in stock_data1]
            dates2 = [stock['date'] for stock in stock_data2]
            prices2 = [stock['close'] for stock in stock_data2]

            # Create a plotly figure
            fig = go.Figure()

            fig.add_trace(go.Scatter(x=dates1, y=prices1, mode='lines', name=f'{symbol1} Closing Price'))
            fig.add_trace(go.Scatter(x=dates2, y=prices2, mode='lines', name=f'{symbol2} Closing Price'))

            fig.update_layout(
                title=f'Stock Price Comparison: {symbol1} vs {symbol2}',
                xaxis_title='Date',
                yaxis_title='Closing Price'
            )

            plot_html = fig.to_html(full_html=False)

            return render_template(
                'comparison.html',
                symbol1=symbol1,
                symbol2=symbol2,
                plot_html=plot_html
            )
        else:
            error_message = 'Could not retrieve data for one or both stocks.'
            return render_template('index.html', error_message=error_message)

    return "Error: Stock symbols not provided."
# Prediction function
def predict_stock_prices(dates, prices):
    dates = pd.to_datetime(dates).map(lambda date: date.to_julian_date()).values.reshape(-1, 1)
    prices = np.array(prices).reshape(-1, 1)

    model = LinearRegression()
    model.fit(dates, prices)

    # Predict the next 5 days
    future_dates = np.array([dates[-1][0] + i for i in range(1, 6)]).reshape(-1, 1)  # Corrected future_dates
    future_prices = model.predict(future_dates)

    future_dates_converted = pd.to_datetime(future_dates.flatten(), origin='julian', unit='D')  # Fix conversion

    return future_dates_converted.strftime('%Y-%m-%d').tolist(), future_prices.flatten().tolist()

# Add prediction visualization function
def plot_predicted_stock(dates, prices, future_dates, future_prices):
    plt.figure(figsize=(10, 6))

    # Convert historical dates to proper datetime format
    dates_converted = pd.to_datetime(dates)  # Convert historical dates

    # Check if future_dates need to be converted (if they are numeric or a different format)
    try:
        future_dates_converted = pd.to_datetime(future_dates)  # Try direct conversion
    except (ValueError, TypeError):
        # Handle numeric date formats (if future_dates are in float or int format representing days)
        future_dates_converted = pd.to_datetime(future_dates, unit='D', origin='1970-01-01')  # Change origin if needed

    # Plot historical data
    plt.plot(dates_converted, prices, marker='o', linestyle='-', color='b', label='Historical Prices')

    # Plot predicted data
    plt.plot(future_dates_converted, future_prices, marker='x', linestyle='--', color='r', label='Predicted Prices')

    # Customize plot
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Price Prediction for Next 5 Days')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the figure
    plt.savefig('static/predicted_stock.png')
    plt.close()

# Plot closing price trend
def plot_closing_price(dates, prices):
    plt.figure(figsize=(10, 6))
    plt.plot(pd.to_datetime(dates), prices, marker='o', linestyle='-', color='b', label='Closing Price')
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.title('Closing Price Trend')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/closing_price.png')
    plt.close()

# Plot volume trend
def plot_volume(dates, volumes):
    plt.figure(figsize=(10, 6))
    plt.bar(pd.to_datetime(dates), volumes, color='g')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.title('Volume Trend')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/volume_chart.png')
    plt.close()

# Plot stock box plot
def plot_boxplot(prices):
    plt.figure(figsize=(6, 4))
    plt.boxplot(prices)
    plt.title('Stock Closing Price Distribution')
    plt.savefig('static/boxplot.png')
    plt.close()

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)


