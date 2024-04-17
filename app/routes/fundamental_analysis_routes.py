from flask import Blueprint, request, Response, abort
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