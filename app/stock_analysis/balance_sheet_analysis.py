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
