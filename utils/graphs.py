import plotly.graph_objs as go
import plotly.subplots as sp
import plotly.express as px
import pandas as pd
import numpy as np
import networkx as nx
from pyvis.network import Network


def plot_heatmap_monthly_changes(monthly_changes):
    """
    Plot a heatmap of monthly changes using Plotly.

    :param monthly_changes: DataFrame with monthly returns
    """
    # Reset index for heatmap plotting
    heatmap_data = monthly_changes.reset_index()
    heatmap_data = heatmap_data.dropna()

    # Extract the company names for y-axis (after resetting index)
    companies = heatmap_data.columns[1:]

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
            y=1.05,  # Position slightly above the graph
            xanchor="center",
            yanchor="bottom",
            thickness=15,  # Adjust the thickness of the color bar
            len=0.5,  # Adjust the length of the color bar
            title_font=dict(size=12),  # Font size for the title
            tickfont=dict(size=10),  # Font size for the tick labels
        ),
        yaxis=dict(
            tickmode="array",  # Use array mode to force showing all companies
            tickvals=list(
                range(len(companies))
            ),  # Set tick values to all company indices
            ticktext=companies,  # Set tick text to company names
            automargin=True,  # Ensure enough margin for the y-axis
        ),
    )

    # Disable interactivity
    fig.update_layout(dragmode=False)

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


def gdp_per_state(df, year):
    min_gdp = df["GDP"].min()
    max_gdp = df["GDP"].max()
    df = df[df["Year"] == str(year)]

    # Check if the filtered DataFrame is empty
    if df.empty:
        print(f"No data available for the year {year}.")
        return

    # Create the choropleth map using go.Figure
    fig = go.Figure(
        data=go.Choropleth(
            locations=df["State"],  # Spatial coordinates (state codes)
            z=df["GDP"],  # Data to be color-coded
            zmin=min_gdp,  # Minimum value for color scale
            zmax=max_gdp,  # Maximum value for color scale
            locationmode="USA-states",  # Set of locations match entries in `locations`
            colorscale="Blues",  # Color scale for GDP
            colorbar_title="GDP in Billions USD",  # Title for the color bar
        )
    )

    # Update layout for the figure
    fig.update_layout(
        title_text=f"GDP by State ({year})",  # Set the initial title
        geo=dict(
            scope="usa",  # Limit map scope to USA
            projection=go.layout.geo.Projection(
                type="albers usa"
            ),  # Albers USA projection
            showlakes=False,  # Show lakes
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

    # Disable interactivity# Disable interactivity
    fig.update_layout(dragmode=False)

    # Show the figure
    return fig


def plot_top_growing_companies():
    """
    Plot an animated scatter plot showing the top 100 growing companies in the USA.

    :param df: DataFrame containing company growth data with columns 'Company', 'Growth', 'Longitude', 'Latitude'.
    """
    df = pd.read_csv(
        "https://raw.githubusercontent.com/plotly/datasets/master/2014_us_cities.csv"
    )
    df.head()

    df["text"] = (
        df["name"] + "<br>Population " + (df["pop"] / 1e6).astype(str) + " million"
    )
    limits = [(0, 3), (3, 11), (11, 21), (21, 50), (50, 3000)]
    colors = ["royalblue", "crimson", "lightseagreen", "orange", "lightgrey"]
    cities = []
    scale = 5000

    fig = go.Figure()

    for i in range(len(limits)):
        lim = limits[i]
        df_sub = df[lim[0] : lim[1]]
        fig.add_trace(
            go.Scattergeo(
                locationmode="USA-states",
                lon=df_sub["lon"],
                lat=df_sub["lat"],
                text=df_sub["text"],
                marker=dict(
                    size=df_sub["pop"] / scale,
                    color=colors[i],
                    line_color="rgb(40,40,40)",
                    line_width=0.5,
                    sizemode="area",
                ),
                name="{0} - {1}".format(lim[0], lim[1]),
            )
        )

    # Update layout for the map
    fig.update_layout(
        title_text="US Population Statistics for 2014",
        showlegend=True,
        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="bottom",
            y=1.03,  # Position above the graph
            xanchor="center",
            x=0.5,  # Center the legend
            bgcolor="rgba(0,0,0,0)",  # Transparent background
            bordercolor="rgba(0,0,0,0)",  # No border color
        ),
        geo=dict(
            scope="usa",
            landcolor="rgb(217, 217, 217)",
            bgcolor="rgba(0,0,0,0)",  # Transparent map background
        ),
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent overall background
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot background
    )

    # Disable interactivity
    fig.update_layout(dragmode=False)

    return fig


def num_tech_companies():
    df = pd.read_csv(
        "https://raw.githubusercontent.com/plotly/datasets/master/1962_2006_walmart_store_openings.csv"
    )

    data = []
    layout = dict(
        title='Number of Tech Companies in US 1962-2006<br>\
    Source: <a href="http://www.econ.umn.edu/~holmes/data/WalMart/index.html">\
    University of Minnesota</a>',
        autosize=False,
        width=1000,
        height=900,
        hovermode=False,
        legend=dict(
            x=0.7,
            y=-0.1,
            bgcolor="rgba(255, 255, 255, 0)",
            font=dict(size=11),
        ),
    )

    years = df["YEAR"].unique()

    for i in range(len(years)):
        geo_key = "geo" + str(i + 1) if i != 0 else "geo"
        lons = list(df[df["YEAR"] == years[i]]["LON"])
        lats = list(df[df["YEAR"] == years[i]]["LAT"])
        # Walmart store data
        data.append(
            dict(
                type="scattergeo",
                showlegend=False,
                lon=lons,
                lat=lats,
                geo=geo_key,
                name=int(years[i]),
                marker=dict(color="rgb(0, 0, 255)", opacity=0.5),
            )
        )
        # Year markers
        data.append(
            dict(
                type="scattergeo",
                showlegend=False,
                lon=[-78],
                lat=[47],
                geo=geo_key,
                text=[years[i]],
                mode="text",
            )
        )
        layout[geo_key] = dict(
            scope="usa",
            showland=True,
            landcolor="rgb(229, 229, 229)",
            showcountries=False,
            domain=dict(x=[], y=[]),
            subunitcolor="rgb(255, 255, 255)",
        )

    def draw_sparkline(domain, lataxis, lonaxis):
        """Returns a sparkline layout object for geo coordinates"""
        return dict(
            showland=False,
            showframe=False,
            showcountries=False,
            showcoastlines=False,
            domain=domain,
            lataxis=lataxis,
            lonaxis=lonaxis,
            bgcolor="rgba(0, 0, 0, 0)",  # Transparent background for sparkline
        )

    # Stores per year sparkline
    layout["geo44"] = draw_sparkline(
        {"x": [0.6, 0.8], "y": [0, 0.15]},
        {"range": [-5.0, 30.0]},
        {"range": [0.0, 40.0]},
    )
    data.append(
        dict(
            type="scattergeo",
            mode="lines",
            lat=list(df.groupby(by=["YEAR"]).count()["storenum"] / 1e1),
            lon=list(range(len(df.groupby(by=["YEAR"]).count()["storenum"] / 1e1))),
            line=dict(color="rgb(0, 0, 255)"),
            name="New companies per year<br>Peak of 178 tech companies per year in 1990",
            geo="geo44",
        )
    )

    # Cumulative sum sparkline
    layout["geo45"] = draw_sparkline(
        {"x": [0.8, 1], "y": [0, 0.15]}, {"range": [-5.0, 50.0]}, {"range": [0.0, 50.0]}
    )
    data.append(
        dict(
            type="scattergeo",
            mode="lines",
            lat=list(df.groupby(by=["YEAR"]).count().cumsum()["storenum"] / 1e2),
            lon=list(range(len(df.groupby(by=["YEAR"]).count()["storenum"] / 1e1))),
            line=dict(color="rgb(214, 39, 40)"),
            name="Cumulative sum<br>3176 tech companies total in 2006",
            geo="geo45",
        )
    )

    z = 0
    COLS = 5
    ROWS = 9
    for y in reversed(range(ROWS)):
        for x in range(COLS):
            geo_key = "geo" + str(z + 1) if z != 0 else "geo"
            layout[geo_key]["domain"]["x"] = [
                float(x) / float(COLS),
                float(x + 1) / float(COLS),
            ]
            layout[geo_key]["domain"]["y"] = [
                float(y) / float(ROWS),
                float(y + 1) / float(ROWS),
            ]
            layout[geo_key][
                "bgcolor"
            ] = "rgba(0, 0, 0, 0)"  # Transparent background for each inner graph
            layout[geo_key]["landcolor"] = "rgb(229, 229, 229)"
            z += 1

    # Create the figure and add data
    fig = go.Figure(data=data, layout=layout)
    # Disable interactivity
    fig.update_layout(
        dragmode=False,
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent overall background
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot background
    )

    return fig


def create_pyvis_network_graph(G, selected_company):
    # Create a color map for industries globally
    unique_industries = set(nx.get_node_attributes(G, "Industry").values())
    color_scale = px.colors.qualitative.Plotly
    industry_color_map = {
        industry: color_scale[i % len(color_scale)]
        for i, industry in enumerate(unique_industries)
    }

    # Create a Pyvis Network object
    net = Network(height="600px", width="800px", notebook=True)

    # Get the subgraph for the selected company or use the full graph
    if selected_company == "All Companies":
        subgraph = G
    elif selected_company in G:
        subgraph = nx.ego_graph(G, selected_company, radius=1, undirected=True)
    else:
        subgraph = G  # Fallback to full graph if selection is invalid

    # Add nodes and edges to the Pyvis network
    for node in subgraph.nodes():
        industry = G.nodes[node]["Industry"]
        net.add_node(
            node,
            label=node,
            title=f"Industry: {industry}",
            color=industry_color_map[industry],
        )

    for edge in subgraph.edges():
        net.add_edge(edge[0], edge[1])

    # Generate the HTML for the Pyvis graph
    html = net.generate_html()

    # Add custom CSS for transparent background and centering
    custom_style = """
    <style>
        #mynetwork {
            background-color: rgba(255, 255, 255, 0); /* Transparent background */
            margin: auto; /* Center the graph */
            display: block; /* Make it a block element */
        }
    </style>
    """
    
    return custom_style + html
