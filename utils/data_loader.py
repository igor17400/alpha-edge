import numpy as np
import pandas as pd
from openbb import obb
import datetime

# General configs
obb.user.preferences.output_type = "dataframe"


def load_stock_data(ticker, start_date, provider):
    """
    Load stock data using OpenBB API or any other API.

    :param ticker: Stock ticker symbol
    :param provider: Data provider for stock data
    :return: DataFrame with stock data
    """
    # Replace with your actual data loading logic
    df = obb.equity.price.historical(ticker, start_date, provider=provider)
    return df


def calculate_monthly_returns(tickers, provider):
    """
    Calculate monthly returns for given tickers and return a DataFrame.

    :param tickers: List of stock ticker symbols
    :param provider: Data provider for stock data
    :return: DataFrame with monthly returns for all tickers
    """
    data_store = {}  # Dictionary to store dataframes for each ticker

    # Define the date range
    end_date = pd.Timestamp.today()  # Today
    start_date = end_date - pd.DateOffset(years=10)
    start_date = start_date.strftime("%Y-%m-%d")

    for ticker in tickers:
        # Load stock data
        df = load_stock_data(ticker, start_date, provider=provider)

        # Ensure index is a datetime index
        df.index = pd.to_datetime(df.index)

        # Resample to get last price of each month
        monthly_price = df["close"].resample("ME").last()

        # Calculate monthly percentage change
        monthly_return = monthly_price.pct_change() * 100  # Convert to percentage

        # Store monthly return DataFrame in the dictionary
        data_store[ticker] = monthly_return

    # Combine all monthly returns into a single DataFrame
    combined_df = pd.DataFrame(data_store)

    return combined_df


def load_state_gdp():
    df = pd.read_csv("./datasets/combined_summary_2000_2023.csv")
    melted_data = df.melt(
        id_vars=["GeoFIPS", "State", "GeoName", "Unit"],
        value_vars=[str(year) for year in range(2000, 2024)],
        var_name="Year",
        value_name="GDP",
    )

    return melted_data
