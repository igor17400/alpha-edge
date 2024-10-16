import plotly.graph_objs as go
import plotly.subplots as sp
import plotly.express as px


def plot_heatmap_monthly_changes(monthly_changes):
    """
    Plot a heatmap of monthly changes using Plotly.

    :param monthly_changes: DataFrame with monthly returns
    """
    # Reset index for heatmap plotting
    heatmap_data = monthly_changes.reset_index()
    heatmap_data = heatmap_data.dropna()

    # Create heatmap using Plotly
    fig = px.imshow(
        heatmap_data.set_index("date").T,  # Transpose for proper orientation
        labels=dict(x="Months", y="Companies", color="Monthly Return (%)"),
        color_continuous_scale="Spectral",
    )

    # Update layout for transparency and color bar positioning
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor= "rgba(0, 0, 0, 0)",
        xaxis_title="Months",
        yaxis_title="Companies",
        coloraxis_colorbar=dict(
            title="Return (%)",
            orientation="h",  # Horizontal color bar
            x=0.5,  # Center the color bar horizontally
            y=1.1,  # Position above the graph
            xanchor="center",
            yanchor="bottom",
        ),
    )

    return fig


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
