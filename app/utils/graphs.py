import plotly.graph_objs as go
import plotly.subplots as sp
import plotly.express as px
import pandas as pd
import numpy as np


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
        paper_bgcolor="rgba(0, 0, 0, 0)",
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


def gdp_per_state():
    # List of US state codes (ISO 3166-2:US)
    states = [
        "AL",
        "AK",
        "AZ",
        "AR",
        "CA",
        "CO",
        "CT",
        "DE",
        "FL",
        "GA",
        "HI",
        "ID",
        "IL",
        "IN",
        "IA",
        "KS",
        "KY",
        "LA",
        "ME",
        "MD",
        "MA",
        "MI",
        "MN",
        "MS",
        "MO",
        "MT",
        "NE",
        "NV",
        "NH",
        "NJ",
        "NM",
        "NY",
        "NC",
        "ND",
        "OH",
        "OK",
        "OR",
        "PA",
        "RI",
        "SC",
        "SD",
        "TN",
        "TX",
        "UT",
        "VT",
        "VA",
        "WA",
        "WV",
        "WI",
        "WY",
    ]

    # Generate random GDP data for 10 years (2010-2020) for each state
    years = np.arange(2010, 2020)
    gdp_data = {
        "State": np.repeat(states, len(years)),  # Repeat each state for each year
        "Year": np.tile(years, len(states)),  # Repeat the years for each state
        "GDP": np.random.randint(
            500, 4000, size=len(states) * len(years)
        ),  # Random GDP values in billions
    }

    # Convert to DataFrame
    data = pd.DataFrame(gdp_data)

    # Create the animated choropleth map
    fig = px.choropleth(
        data_frame=data,
        locations="State",  # State codes
        locationmode="USA-states",  # Mode for state-level mapping
        color="GDP",  # The data to color the states by (GDP in this case)
        animation_frame="Year",  # Animate over the 'Year' column
        color_continuous_scale="Blues",  # Color scale for GDP
        range_color=(
            data["GDP"].min(),
            data["GDP"].max(),
        ),  # Range of colors based on GDP values
        scope="usa",  # Focus on USA
        labels={"GDP": "GDP in Billions USD"},  # Label for the color legend
    )

    # Prepare frames for animation
    frames = []
    for year in years:
        frame_data = data[data["Year"] == year]
        frames.append(
            go.Frame(
                data=[
                    go.Choropleth(
                        locations=frame_data["State"],
                        z=frame_data["GDP"],
                        locationmode="USA-states",
                        colorscale="Blues",
                        showscale=False,  # Hide color scale in each frame
                    )
                ],
                layout=go.Layout(
                    title_text=f"GDP in {year}",  # Update title for the frame
                ),
            )
        )

    # Add the frames to the figure
    fig.frames = frames

    # Set the animation to autoplay and loop automatically without buttons or sliders
    fig["layout"].pop("updatemenus")
    fig["layout"]["sliders"] = []  # Remove the slider

    # Update layout to remove title, buttons, sliders, and set transparent background
    fig.update_layout(
        title_text="USA GDP in 2010",  # Set the initial title
        geo=dict(
            scope="usa",
            projection=go.layout.geo.Projection(
                type="albers usa"
            ),  # Albers USA projection
            showlakes=False,  # Hide lakes
            bgcolor="rgba(0,0,0,0)",  # Transparent map background
        ),
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent overall background
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot background
        coloraxis_colorbar=dict(
            ticks="outside",  # Put ticks outside for better visualization
            ticklen=5,
            tickwidth=2,
        ),
    )
    # Disable interactivity
    fig.update_layout(dragmode=False)

    return fig
