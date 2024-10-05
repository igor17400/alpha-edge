from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from utils.data_loader import load_main_indices_stock_data


def register_callbacks(app):
    @app.callback(
        Output("market-overview-graph", "figure"), Input("market-overview-graph", "id")
    )
    def update_market_overview(dummy):
        # Load main indices stock data
        indices = load_main_indices_stock_data()

        # Create an empty list to hold individual index DataFrames
        dataframes = []

        # Loop through each index in the dictionary to prepare the data for plotting
        for index_name, df in indices.items():
            # Check if DataFrame has the required data
            if not df.empty and "date" in df.columns and "close" in df.columns:
                # Add a new column to distinguish each index and select relevant columns
                df["Index"] = index_name
                dataframes.append(df[["date", "close", "Index"]])

        # Combine all index DataFrames into a single DataFrame
        combined_df = pd.concat(dataframes, ignore_index=True)

        # Create a line chart for all indices using 'Index' to differentiate lines
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
