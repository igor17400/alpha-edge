from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import config
import time

from layout import create_layout
from utils.apis import verify_api_credentials


def register_callbacks(app):
    @app.callback(
        [
            Output("app-content", "children"),
            Output("market-overview-graph", "style"),
            Output("stock-selector", "style"),
            Output("stock-comparison-graph", "style"),
        ],
        Input("loading-screen", "children"),
    )
    def load_app_content(_):
        api_status = verify_api_credentials(config.OPENBB_TOKEN)

        if api_status == "success":
            # Show the real layout when API is verified
            return (
                "",
                create_layout(),
                {"display": "block"},
                {"display": "block"},
                {"display": "block"},
            )
        elif api_status == "fail":
            return (
                "",
                html.Div(
                    [
                        html.H1("API Credentials Not Loaded", style={"color": "red"}),
                        html.P(
                            "Failed to load API credentials. Please check your API token and try again."
                        ),
                        html.P(
                            "If the issue persists, ensure that the token is valid and correctly formatted."
                        ),
                    ],
                    style={"textAlign": "center", "marginTop": "50px"},
                ),
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
            )
        else:
            # If there was an error during login, show the error message
            return (
                "",
                html.Div(
                    [
                        html.H1("Error During API Login", style={"color": "red"}),
                        html.P(
                            f"An error occurred while attempting to log in: {api_status.split(': ')[1]}"
                        ),
                        html.P(
                            "Please check your API credentials or contact support if the issue persists."
                        ),
                    ],
                    style={"textAlign": "center", "marginTop": "50px"},
                ),
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
            )

    # @app.callback(
    #     Output("stock-comparison-graph", "figure"), Input("stock-selector", "value")
    # )
    # def update_stock_comparison(selected_stocks):
    #     # Placeholder data - replace with actual data loading
    #     df = pd.DataFrame(
    #         {
    #             "Date": pd.date_range(start="2022-01-01", periods=100),
    #             "PETR4": np.random.randint(20, 30, 100),
    #             "VALE3": np.random.randint(70, 90, 100),
    #             "ITUB4": np.random.randint(20, 25, 100),
    #         }
    #     )
    #     fig = px.line(df, x="Date", y=selected_stocks, title="Stock Price Comparison")
    #     return fig

    # @app.callback(
    #     [
    #         Output("market-overview-graph", "figure"),
    #         Output("grid1-bvsp-vs-gspc", "figure"),
    #         Output("grid2-bvsp-vs-ixic", "figure"),
    #         Output("grid3-bvsp-vs-dji", "figure"),
    #     ],
    #     Input("market-overview-graph", "id"),
    # )
    # def update_all_graphs(dummy):
    #     # Load main indices stock data
    #     indices = load_main_indices_stock_data()

    #     # Handle errors and empty data
    #     if not indices:
    #         empty_figure = px.line(
    #             title="Failed to load stock data. Please try again later."
    #         )
    #         return empty_figure, empty_figure, empty_figure, empty_figure

    #     # Combine data for major indices for the main "Performance of Major Stock Indices" graph
    #     dataframes = []
    #     for index_name, df in indices.items():
    #         if not df.empty:
    #             df["Index"] = index_name
    #             dataframes.append(df[["date", "close", "Index"]])

    #     combined_df = pd.concat(dataframes, ignore_index=True)

    #     # Create the main overview line chart for all indices
    #     main_fig = px.line(
    #         combined_df,
    #         x="date",
    #         y="close",
    #         color="Index",
    #         title="Performance of Major Stock Indices",
    #     )

    #     # Create comparison grids for each pair of indices
    #     grid1_fig = create_comparison_figure(
    #         indices["^BVSP"], indices["^GSPC"], "Grid 1: S&P 500 vs IBOVESPA"
    #     )
    #     grid2_fig = create_comparison_figure(
    #         indices["^BVSP"], indices["^IXIC"], "Grid 2: NASDAQ vs IBOVESPA"
    #     )
    #     grid3_fig = create_comparison_figure(
    #         indices["^BVSP"], indices["^DJI"], "Grid 3: Dow Jones vs IBOVESPA"
    #     )

    #     return main_fig, grid1_fig, grid2_fig, grid3_fig
