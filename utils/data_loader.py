import pandas as pd
from openbb import obb


def load_stock_data(ticker, start_date, end_date, provider):
    """
    Load stock data using OpenBB API.

    :param ticker: Stock ticker symbol
    :param start_date: Start date for data retrieval
    :param end_date: End date for data retrieval
    :param provider: Data provider for stock data
    :return: DataFrame with stock data
    """
    df = obb.stocks.load(
        ticker=ticker, start_date=start_date, end_date=end_date, provider=provider
    )
    return df
