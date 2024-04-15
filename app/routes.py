from app import app, db
from flask import Blueprint, request, Response, jsonify, redirect, url_for, flash
from datetime import datetime, timedelta
import json
import logging


from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from app.models import User
import app.stock_analysis.technical_analysis as technical_analyses

api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    logging.info(f"Received login request with data: {data}")
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user is None or not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@api_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    user = User(username=username, email=email)
    user.password = generate_password_hash(password)
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 201
@api_routes.route('/forecast', methods=['GET'])
def forecast():
    """
    Endpoint to generate and return a forecast chart for a given stock ticker symbol.

    Returns:
    flask.Response: Flask response containing the forecast chart as a PNG image.
    """
    data = request.get_json()
    ticker = data.get('ticker', 'PETKM.IS')  
    model = technical_analyses.create_prophet_model(ticker)
    forecast = technical_analyses.make_forecast(model, 365)
    return technical_analyses.make_forecast_chart(model, forecast)


@api_routes.route('/dataDatePeriod', methods=['GET'])
def data_date_period():
    """
    Endpoint to fetch historical stock data for a given stock ticker symbol within a specified date range.

    Returns:
    flask.Response: Flask response containing historical stock data as JSON.
    """
    data = request.get_json()
    ticker = data.get('ticker', 'PETKM.IS')  

    # Get the start and end dates from the JSON data
    start = data.get('start', (datetime.now() - timedelta(days=5*365)).strftime('%Y-%m-%d'))  
    end = data.get('end', datetime.now().strftime('%Y-%m-%d'))  

    stock_value = technical_analyses.get_stock_historical_info(ticker, start, end)

    stock_value_json =  stock_value.reset_index().to_json(date_format='iso', orient='records')
    stock_value_json = json.dumps(json.loads(stock_value_json))
    # Create a response with the JSON data
    return Response(stock_value_json, mimetype='application/json')

@api_routes.route('/dataPeriod', methods=['GET'])
def data_period():
    """
    Endpoint to fetch historical stock data for a given stock ticker symbol within a specified period.

    Returns:
    flask.Response: Flask response containing historical stock data as JSON.
    """
    data = request.get_json()
    ticker = data.get('ticker', 'PETKM.IS')  
    period = data.get('period', 'max')
    stock_value = technical_analyses.get_stock_data(ticker, period)

    stock_value_json =  stock_value.reset_index().to_json(date_format='iso', orient='records')
    stock_value_json = json.dumps(json.loads(stock_value_json))
    # Create a response with the JSON data
    return Response(stock_value_json, mimetype='application/json')

