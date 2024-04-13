from flask import send_file
from datetime import datetime
from pandas_datareader import data as pdr
import yfinance as yf
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import numpy as np
import io

yf.pdr_override()

df = pd.DataFrame()

def get_stock_historical_info(stock , start_date, end_date):
	if isinstance(start_date, str):
		start_date = datetime.strptime(start_date, '%Y-%m-%d')
		
	if isinstance(end_date, str):
		end_date = datetime.strptime(end_date, '%Y-%m-%d')

	stock_value = pdr.get_data_yahoo(stock, start=start_date, end=end_date)
	return stock_value

def get_stock_data(stock, period="max"):
	stock_info = yf.Ticker(stock)
	all_data = stock_info.history(period=period, auto_adjust=True)
	return all_data

def create_prophet_model(ticker, hist='max'):
	# create new data frame to hold dates (ds) & adjusted closing prices (y)
	stock_data = yf.Ticker(ticker)

	hist_data = stock_data.history(hist, auto_adjust=True)

	df = pd.DataFrame()

	df['ds'] = hist_data.index.values
	df['y'] = hist_data['Close'].values

	# create a Prophet model from that data
	model = Prophet(
		changepoint_prior_scale=0.05,
		holidays_prior_scale=15,
		seasonality_prior_scale=10,
		weekly_seasonality=True,
		yearly_seasonality=True,
		daily_seasonality=False
	)

	country = get_country_from_ticker(ticker)
	model.add_country_holidays(country_name=country)
	model.fit(df)

	return model

def make_forecast(model, periods):
	future = model.make_future_dataframe(periods, freq='D')
	forecast = model.predict(future)
	return forecast

def make_forecast_chart(model, forecast):
	fig = model.plot_components(forecast)
	#Save the figure to a BytesIO object
	buf = io.BytesIO()
	plt.savefig(buf, format='png')
	plt.close(fig)  # Close the figure to free up memory
	buf.seek(0)
	return send_file(buf, mimetype='image/png')

def get_country_from_ticker(ticker):
    if '.IS' in ticker:
        return 'TR'
    elif '.TO' in ticker:
        return 'CA'
    else:
        return 'US'