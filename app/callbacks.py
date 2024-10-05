from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from utils.data_loader import load_main_indices_stock_data
import time


def register_callbacks(app):
    @app.callback(
        Output("market-overview-graph", "figure"), Input("market-overview-graph", "id")
    )
    def update_market_overview(dummy):
        # Step 1: Load main indices stock data and handle empty or None response
        max_retries = 3
        retry_count = 0
        indices = None

        while indices is None and retry_count < max_retries:
            indices = load_main_indices_stock_data()
            retry_count += 1
            if indices is None or not indices:
                time.sleep(
                    1
                )  # Wait for 1 second before retrying (to avoid rapid retry loops)

        # If the data could not be loaded, return an error message
        if indices is None or not indices:
            return px.line(title="Failed to load stock data. Please try again later.")

        # Step 2: Create an empty list to hold individual index DataFrames
        dataframes = []

        # Step 3: Loop through each index in the dictionary to prepare the data for plotting
        for index_name, df in indices.items():
            # Check if DataFrame has the required data
            if not df.empty and "date" in df.columns and "close" in df.columns:
                # Add a new column to distinguish each index and select relevant columns
                df["Index"] = index_name
                dataframes.append(df[["date", "close", "Index"]])

        # Step 4: Check if the dataframes list is empty before combining
        if not dataframes:
            return px.line(title="No data available for the selected indices.")

        # Step 5: Combine all index DataFrames into a single DataFrame
        combined_df = pd.concat(dataframes, ignore_index=True)

        # Step 6: Create a line chart for all indices using 'Index' to differentiate lines
        fig = px.line(
            combined_df,
            x="date",
            y="close",
            color="Index",
            title="Performance of Major Stock Indices",
            labels={"close": "Closing Price", "date": "Date", "Index": "Index Name"},
        )

        return fig

    @app.callback(
        Output("stock-comparison-graph", "figure"), Input("stock-selector", "value")
    )
    def update_stock_comparison(selected_stocks):
        # Placeholder data - replace with actual data loading
        df = pd.DataFrame(
            {
                "Date": pd.date_range(start="2022-01-01", periods=100),
                "PETR4": np.random.randint(20, 30, 100),
                "VALE3": np.random.randint(70, 90, 100),
                "ITUB4": np.random.randint(20, 25, 100),
            }
        )
        fig = px.line(df, x="Date", y=selected_stocks, title="Stock Price Comparison")
        return fig
