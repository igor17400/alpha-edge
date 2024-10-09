from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import plotly.subplots as sp
import pandas as pd
import numpy as np
from utils.data_loader import load_main_indices_stock_data


def create_comparison_figure(ibov_df, index_df, title):
    # Calculate required metrics for the comparison
    rolling_corr = ibov_df["close"].rolling(50).corr(index_df["close"])
    price_ratio = ibov_df["close"] / index_df["close"]
    rolling_std_ibov = ibov_df["close"].rolling(50).std()
    rolling_std_index = index_df["close"].rolling(50).std()
    cumulative_returns_ibov = (1 + ibov_df["close"].pct_change()).cumprod()
    cumulative_returns_index = (1 + index_df["close"].pct_change()).cumprod()

    # Create a 2x2 subplot figure with a shared axis template
    fig = sp.make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "50-Day Rolling Correlation",
            "Price Ratio",
            "Volatility",
            "Cumulative Returns",
        ),
        horizontal_spacing=0.1,  # Adjust for even spacing between subplots
        vertical_spacing=0.2,
    )

    # Plot each metric in the subplots
    fig.add_trace(
        go.Scatter(
            x=ibov_df["date"],
            y=rolling_corr,
            name="50-Day Rolling Correlation",
            mode="lines",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(x=ibov_df["date"], y=price_ratio, name="Price Ratio", mode="lines"),
        row=1,
        col=2,
    )
    fig.add_trace(
        go.Scatter(
            x=ibov_df["date"], y=rolling_std_ibov, name="IBOV Volatility", mode="lines"
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=index_df["date"],
            y=rolling_std_index,
            name="Index Volatility",
            mode="lines",
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=ibov_df["date"],
            y=cumulative_returns_ibov,
            name="IBOV Cumulative Returns",
            mode="lines",
        ),
        row=2,
        col=2,
    )
    fig.add_trace(
        go.Scatter(
            x=index_df["date"],
            y=cumulative_returns_index,
            name="Index Cumulative Returns",
            mode="lines",
        ),
        row=2,
        col=2,
    )

    # Update layout for the figure
    fig.update_layout(
        height=800,
        width=1000,
        title_text=title,
        template="plotly_white",  # Use a white template instead of plotly_dark
        paper_bgcolor="white",  # Set the outer background to white
        plot_bgcolor="white",  # Set the plotting area background to white
        font=dict(color="black"),  # Change font color to black
        xaxis=dict(showgrid=True, gridcolor="lightgrey", zerolinecolor="lightgrey"),
        yaxis=dict(showgrid=True, gridcolor="lightgrey", zerolinecolor="lightgrey"),
        legend=dict(bgcolor="white", bordercolor="lightgrey"),
    )

    return fig


def register_callbacks(app):
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

    @app.callback(
        [
            Output("market-overview-graph", "figure"),
            Output("grid1-bvsp-vs-gspc", "figure"),
            Output("grid2-bvsp-vs-ixic", "figure"),
            Output("grid3-bvsp-vs-dji", "figure"),
        ],
        Input("market-overview-graph", "id"),
    )
    def update_all_graphs(dummy):
        # Load main indices stock data
        indices = load_main_indices_stock_data()

        # Handle errors and empty data
        if not indices:
            empty_figure = px.line(
                title="Failed to load stock data. Please try again later."
            )
            return empty_figure, empty_figure, empty_figure, empty_figure

        # Combine data for major indices for the main "Performance of Major Stock Indices" graph
        dataframes = []
        for index_name, df in indices.items():
            if not df.empty:
                df["Index"] = index_name
                dataframes.append(df[["date", "close", "Index"]])

        combined_df = pd.concat(dataframes, ignore_index=True)

        # Create the main overview line chart for all indices
        main_fig = px.line(
            combined_df,
            x="date",
            y="close",
            color="Index",
            title="Performance of Major Stock Indices",
        )

        # Create comparison grids for each pair of indices
        grid1_fig = create_comparison_figure(
            indices["^BVSP"], indices["^GSPC"], "Grid 1: S&P 500 vs IBOVESPA"
        )
        grid2_fig = create_comparison_figure(
            indices["^BVSP"], indices["^IXIC"], "Grid 2: NASDAQ vs IBOVESPA"
        )
        grid3_fig = create_comparison_figure(
            indices["^BVSP"], indices["^DJI"], "Grid 3: Dow Jones vs IBOVESPA"
        )

        return main_fig, grid1_fig, grid2_fig, grid3_fig
