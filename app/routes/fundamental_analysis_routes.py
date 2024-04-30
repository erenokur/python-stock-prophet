from flask import Blueprint, request, Response, abort
from yfinance.exceptions import YFNotImplementedError
import pandas as pd
import numpy as np
import datetime
import json

from app.responses import bad_request_ticker_response
import app.stock_analysis.fundamental_analysis as fundamental_analysis

fundamental_analysis_routes = Blueprint('fundamental_analysis_routes', __name__)

@fundamental_analysis_routes.route('/getStockBalanceSheet', methods=['GET'])
def get_stock_balance_sheet():
    """
    Fetches the balance sheet data for a given stock ticker symbol.

    Args:
    ticker (str): The stock ticker symbol to fetch balance sheet data for.

    Returns:
    pandas.DataFrame: The balance sheet data for the given stock ticker symbol.
    """
    data = request.get_json()
    ticker = data.get('ticker')
    if not ticker:
        return bad_request_ticker_response()
    # Fetch balance sheet data
    stock_balance_sheet = fundamental_analysis.get_stock_balance_sheet(ticker)
    stock_balance_sheet_dict = stock_balance_sheet.to_dict()
    # Convert Timestamp objects in keys to strings
    stock_balance_sheet_dict = {str(key): value for key, value in stock_balance_sheet_dict.items()}
    # Structure the dictionary
    structured_dict = {'stock_quarters': stock_balance_sheet_dict}
    structured_json = json.dumps(structured_dict)

    return Response(structured_json, mimetype='application/json')

@fundamental_analysis_routes.route('/getStockCashFlow', methods=['GET'])
def get_stock_cash_flow():
    """
    Fetches the cash flow data for a given stock ticker symbol.

    Args:
    ticker (str): The stock ticker symbol to fetch cash flow data for.

    Returns:
    pandas.DataFrame: The cash flow data for the given stock ticker symbol.
    """
    data = request.get_json()
    ticker = data.get('ticker')
    if not ticker:
        return bad_request_ticker_response()
    # Fetch cash flow data
    stock_cash_flow = fundamental_analysis.get_stock_cash_flow(ticker)
    stock_cash_flow_dict = stock_cash_flow.to_dict()
    # Convert Timestamp objects in keys to strings
    stock_cash_flow_dict = {str(key): value for key, value in stock_cash_flow_dict.items()}
    # Structure the dictionary
    structured_dict = {'stock_quarters': stock_cash_flow_dict}
    structured_json = json.dumps(structured_dict)

    return Response(structured_json, mimetype='application/json')

@fundamental_analysis_routes.route('/getStockIncomeStatement', methods=['GET'])
def get_stock_income_statement():
    """
    Fetches the income statement data for a given stock ticker symbol.

    Args:
    ticker (str): The stock ticker symbol to fetch income statement data for.

    Returns:
    pandas.DataFrame: The income statement data for the given stock ticker symbol.
    """
    data = request.get_json()
    ticker = data.get('ticker')
    if not ticker:
        return bad_request_ticker_response()
    # Fetch income statement data
    stock_income_statement = fundamental_analysis.get_stock_income_statement(ticker)
    stock_income_statement_dict = stock_income_statement.to_dict()
    # Convert Timestamp objects in keys to strings
    stock_income_statement_dict = {str(key): value for key, value in stock_income_statement_dict.items()}
    # Structure the dictionary
    structured_dict = {'stock_quarters': stock_income_statement_dict}
    structured_json = json.dumps(structured_dict)

    return Response(structured_json, mimetype='application/json')

@fundamental_analysis_routes.route('/getAllStockData', methods=['GET'])
def get_all_stock_data():
    """
    Fetches all the data for a given stock ticker symbol.

    Args:
    ticker (str): The stock ticker symbol to fetch all data for.

    Returns:
    pandas.DataFrame: The balance sheet, cash flow, and income statement data for the given stock ticker symbol.
    """
    data = request.get_json()
    ticker = data.get('ticker')
    if not ticker:
        return bad_request_ticker_response()
    # Fetch all data
    stock_data = fundamental_analysis.get_all_stock_data(ticker)
    # YFNotImplementedError
    skip_props = [
        'analyst_price_target',
        'earnings',
        'eps_est',
        'earnings_forecasts',
        'earnings_trend',
        'quarterly_earnings',
        'revenue_forecasts',
        'shares',
        'sustainability',
        'trend_details',
        'fast_info'
        ]

    data = {}   
    for prop in dir(stock_data):
        if prop in skip_props or prop.startswith('_') or callable(getattr(stock_data, prop)) :
            continue
        value = getattr(stock_data, prop)
        if isinstance(value, pd.DataFrame):
            data[convert_timestamp_keys(prop)] = convert_timestamp_keys(value.to_dict())
        elif isinstance(value, dict):
            data[convert_timestamp_keys(prop)] = convert_timestamp_keys(value)
        elif isinstance(value, pd.Series):
            data[convert_timestamp_keys(prop)] = convert_timestamp_keys(value.to_dict())
        else:
            data[convert_timestamp_keys(prop)] = value
        
    return json.dumps(data)

def convert_timestamp_keys(obj):
    if isinstance(obj, dict):
        return {k.isoformat() if isinstance(k, pd.Timestamp) else k: convert_timestamp_keys(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_timestamp_keys(elem) for elem in obj]
    else:
        return obj
    
def to_json(data):
    if data is None or isinstance(data, (bool, int, tuple, range, str, list)):
        return data
    return str(data)

@fundamental_analysis_routes.route('/evaluateStockValueInIndustry', methods=['GET'])
def evaluate_stock_value_in_industry():
    """
    Performs fundamental analysis on a given stock ticker symbol.

    Args:
    ticker (str): The stock ticker symbol to perform fundamental analysis on.

    Returns:
    str: The result of the fundamental analysis.
    """
    data = request.get_json()
    ticker = data.get('ticker')
    if not ticker:
        return bad_request_ticker_response()
    # Perform fundamental analysis
    analysis_result = fundamental_analysis.evaluate_stock_value_in_industry(ticker)
    structured_dict = {'fundamental_analysis': analysis_result}
    structured_json = json.dumps(structured_dict)

    return Response(structured_json, mimetype='application/json')


@fundamental_analysis_routes.route('/fundamentalAnalysis', methods=['GET'])
def perform_fundamental_analysis():
    """
    Performs fundamental analysis on a given stock ticker symbol.

    Args:
    ticker (str): The stock ticker symbol to perform fundamental analysis on.

    Returns:
    str: The result of the fundamental analysis.
    """
    data = request.get_json()
    ticker = data.get('ticker')
    if not ticker:
        return bad_request_ticker_response()
    # Perform fundamental analysis
    return None
