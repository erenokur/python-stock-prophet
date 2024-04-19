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

def fundamental_analysis(ticker):
    """
    Performs fundamental analysis on a given stock ticker symbol.

    Args:
    ticker (str): The stock ticker symbol.

    Returns:
    str: The result of the fundamental analysis.
    """
    # Fetch necessary data
    balance_sheet = get_stock_balance_sheet(ticker)
    cash_flow = get_stock_cash_flow(ticker)
    income_statement = get_stock_income_statement(ticker)
    ticker_obj = yf.Ticker(ticker)

    results = []

    # Iterate over all quarters
    for i in range(balance_sheet.shape[1]):
        # Select the data for the current quarter
        bs_quarter = balance_sheet.iloc[:, i]
        cf_quarter = cash_flow.iloc[:, i]
        is_quarter = income_statement.iloc[:, i]

        # Calculate ratios
        net_income = is_quarter.loc['Net Income']
        outstanding_shares = ticker_obj.info['sharesOutstanding']
        earnings_per_share = net_income / outstanding_shares
        pe_ratio = ticker_obj.info['currentPrice'] / earnings_per_share

        total_liabilities = bs_quarter.loc['Current Liabilities'] + bs_quarter.loc['Total Non Current Liabilities Net Minority Interest']

        total_equity = bs_quarter.loc['Common Stock Equity'] + bs_quarter.loc['Retained Earnings']

        pb_ratio = ticker_obj.info['currentPrice'] / (bs_quarter.loc['Total Assets'] - total_liabilities) / total_equity

        free_cash_flow = cf_quarter.loc['Free Cash Flow']

        # Compare with industry averages
        industry_pe = ticker_obj.info['trailingPE']
        industry_pb = ticker_obj.info['priceToBook']

        if pe_ratio < industry_pe and pb_ratio < industry_pb:
            results.append("Positive")
        else:
            results.append("Negative")

    return is_company_improving(results)

def is_company_improving(results):
    """
    Checks if the number of positive results is increasing over the quarters.

    Args:
    results (list): The list of results from the fundamental analysis.

    Returns:
    str: 'Positive' if the number of positive results is increasing, 'Negative' otherwise.
    """
    # Count the number of positive results in each quarter
    positive_counts = [results[i:i+4].count('Positive') for i in range(0, len(results), 4)]

    # Check if the counts are increasing
    if all(x<y for x, y in zip(positive_counts, positive_counts[1:])):
        return 'Positive'
    else:
        return 'Negative'