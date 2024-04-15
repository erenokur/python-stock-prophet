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

def get_stock_historical_info(stock, start_date, end_date):
    """
    Fetches historical stock data for a given stock symbol and date range.

    Parameters:
    - stock (str): Stock symbol.
    - start_date (str or datetime): Start date in 'YYYY-MM-DD' format or as a datetime object.
    - end_date (str or datetime): End date in 'YYYY-MM-DD' format or as a datetime object.

    Returns:
    pandas.DataFrame: DataFrame containing the historical stock data.
    """
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    stock_value = pdr.get_data_yahoo(stock, start=start_date, end=end_date)
    return stock_value

def get_stock_data(stock, period="max"):
    """
    Fetches historical stock data for a given stock symbol.

    Parameters:
    - stock (str): Stock symbol.
    - period (str): Period for which historical data should be fetched. Default is "max".

    Returns:
    pandas.DataFrame: DataFrame containing the historical stock data.
    """
    stock_info = yf.Ticker(stock)
    all_data = stock_info.history(period=period, auto_adjust=True)
    return all_data

def create_prophet_model(ticker, hist='max'):
    """
    Creates a Prophet model for stock forecasting based on historical stock data.

    Parameters:
    - ticker (str): Stock ticker symbol.
    - hist (str): Historical period for training the model. Default is 'max'.

    Returns:
    prophet.forecaster.Prophet: Prophet model.
    """
    stock_data = yf.Ticker(ticker)
    hist_data = stock_data.history(hist, auto_adjust=True)

    df = pd.DataFrame()
    df['ds'] = hist_data.index.values
    df['y'] = hist_data['Close'].values

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
    """
    Generates a forecast using the provided Prophet model for a specified number of future periods.

    Parameters:
    - model (prophet.forecaster.Prophet): Prophet model.
    - periods (int): Number of future periods to forecast.

    Returns:
    pandas.DataFrame: DataFrame containing the forecast data.
    """
    future = model.make_future_dataframe(periods, freq='D')
    forecast = model.predict(future)
    return forecast

def make_forecast_chart(model, forecast):
    """
    Generates and returns a chart visualizing the forecast produced by the Prophet model.

    Parameters:
    - model (prophet.forecaster.Prophet): Prophet model.
    - forecast (pandas.DataFrame): DataFrame containing the forecast data.

    Returns:
    flask.Response: Flask response containing the forecast chart as a PNG image.
    """
    fig = model.plot_components(forecast)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

def get_country_from_ticker(ticker):
    """
    Determines the country associated with a given stock ticker symbol.

    Parameters:
    - ticker (str): Stock ticker symbol.

    Returns:
    str: Country code ('US' for United States, 'CA' for Canada, 'TR' for Turkey).
    """
    if '.IS' in ticker:
        return 'TR'
    elif '.TO' in ticker:
        return 'CA'
    else:
        return 'US'
