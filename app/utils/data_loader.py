import pandas as pd
from openbb import obb

def load_main_indices_stock_data():
    # Load data for IBOVESPA and major US indices
    symbols = ["^BVSP", "^GSPC", "^IXIC", "^DJI"]  # IBOVESPA, S&P 500, NASDAQ, Dow Jones
    provider = "yfinance"
    data = {}
    
    for symbol in symbols:
        historical_data = obb.equity.price.historical(symbol=symbol, provider=provider)
        data[symbol] = pd.DataFrame(historical_data).reset_index()

    return data


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
