import yfinance as yf

def get_stock_balance_sheet(ticker):
    """
    Fetches the balance sheet data for a given stock ticker symbol.

    Args:
    ticker (str): The stock ticker symbol.

    Returns:
    pandas.DataFrame: The balance sheet data.
    """
    # Fetch balance sheet data
    balance_sheet = yf.Ticker(ticker).balance_sheet

    return balance_sheet

def get_stock_cash_flow(ticker):
    """
    Fetches the cash flow data for a given stock ticker symbol.

    Args:
    ticker (str): The stock ticker symbol.

    Returns:
    pandas.DataFrame: The cash flow data.
    """
    # Fetch cash flow data
    cash_flow = yf.Ticker(ticker).cashflow

    return cash_flow

def get_stock_income_statement(ticker):
    """
    Fetches the income statement data for a given stock ticker symbol.

    Args:
    ticker (str): The stock ticker symbol.

    Returns:
    pandas.DataFrame: The income statement data.
    """
    # Fetch income statement data
    income_statement = yf.Ticker(ticker).financials

    return income_statement
