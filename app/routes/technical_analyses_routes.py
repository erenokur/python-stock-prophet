from flask import Blueprint, request, Response, jsonify, abort
from datetime import datetime, timedelta
import json

from app.responses import bad_request_ticker_response
import app.stock_analysis.technical_analysis as technical_analyses

technical_analyses_routes = Blueprint('technical_analyses_routes', __name__)

@technical_analyses_routes.route('/forecast', methods=['GET'])
def forecast():
    """
    Endpoint to generate and return a forecast chart for a given stock ticker symbol.

    Returns:
    flask.Response: Flask response containing the forecast chart as a PNG image.
    """
    data = request.get_json()
    ticker = data.get('ticker')
    if not ticker:
        return bad_request_ticker_response()
    
    model = technical_analyses.create_prophet_model(ticker)
    forecast = technical_analyses.make_forecast(model, 365)
    return technical_analyses.make_forecast_chart(model, forecast)

@technical_analyses_routes.route('/dataDatePeriod', methods=['GET'])
def data_date_period():
    """
    Endpoint to fetch historical stock data for a given stock ticker symbol within a specified date range.

    Returns:
    flask.Response: Flask response containing historical stock data as JSON.
    """
    data = request.get_json()
    ticker = data.get('ticker')
    if not ticker:
        return bad_request_ticker_response()

    # Get the start and end dates from the JSON data
    start = data.get('start', (datetime.now() - timedelta(days=5*365)).strftime('%Y-%m-%d'))  
    end = data.get('end', datetime.now().strftime('%Y-%m-%d'))  

    stock_value = technical_analyses.get_stock_historical_info(ticker, start, end)

    stock_value_json =  stock_value.reset_index().to_json(date_format='iso', orient='records')
    stock_value_json = json.dumps(json.loads(stock_value_json))
    # Create a response with the JSON data
    return Response(stock_value_json, mimetype='application/json')

@technical_analyses_routes.route('/dataPeriod', methods=['GET'])
def data_period():
    """
    Endpoint to fetch historical stock data for a given stock ticker symbol within a specified period.

    Returns:
    flask.Response: Flask response containing historical stock data as JSON.
    """
    data = request.get_json()
    ticker = data.get('ticker')
    if not ticker:
        return bad_request_ticker_response()

    period = data.get('period', 'max')
    stock_value = technical_analyses.get_stock_data(ticker, period)

    stock_value_json =  stock_value.reset_index().to_json(date_format='iso', orient='records')
    stock_value_json = json.dumps(json.loads(stock_value_json))
    # Create a response with the JSON data
    return Response(stock_value_json, mimetype='application/json')