import plotly.graph_objs as go
import plotly.subplots as sp
import plotly.express as px
import pandas as pd
import numpy as np
import networkx as nx


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

    # Generate random GDP data
    years = np.arange(2000, 2024)
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
        title_text="USA GDP in 2000",  # Set the initial title
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
        title_text="Number of Companies per State in 2022",
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


def graphs_m_and_a():
    # Let's import the ZKC graph
    ZKC_graph = nx.karate_club_graph()

    # Define constants for the nodes
    Apple = 0
    Microsoft = 33
    Num_nodes = 34

    # Get the club labels
    club_labels = list(nx.get_node_attributes(ZKC_graph, "club").values())

    # Define communities
    community_0 = [8, 14, 15, 18, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]
    community_1 = [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 16, 17, 19, 21]

    # Label for each node corresponds to community 0 or community 1
    community_label = (
        [2] * 12 + [1] * 18 + [0] * 16
    )  # 18 nodes in community 1, 16 in community 0

    # Spring layout for 3D
    spring_3D = nx.spring_layout(ZKC_graph, dim=3, seed=18)

    # Extract coordinates for nodes
    x_nodes = [spring_3D[i][0] for i in range(Num_nodes)]
    y_nodes = [spring_3D[i][1] for i in range(Num_nodes)]
    z_nodes = [spring_3D[i][2] for i in range(Num_nodes)]

    # Create a list of edges for the plot
    edge_list = ZKC_graph.edges()
    x_edges = []
    y_edges = []
    z_edges = []

    # Fill edge coordinates
    for edge in edge_list:
        x_coords = [spring_3D[edge[0]][0], spring_3D[edge[1]][0], None]
        x_edges += x_coords

        y_coords = [spring_3D[edge[0]][1], spring_3D[edge[1]][1], None]
        y_edges += y_coords

        z_coords = [spring_3D[edge[0]][2], spring_3D[edge[1]][2], None]
        z_edges += z_coords

    # Create traces for edges and nodes
    trace_edges = go.Scatter3d(
        x=x_edges,
        y=y_edges,
        z=z_edges,
        mode="lines",
        line=dict(color="black", width=2),
        hoverinfo="none",
    )

    trace_nodes = go.Scatter3d(
        x=x_nodes,
        y=y_nodes,
        z=z_nodes,
        mode="markers",
        marker=dict(
            symbol="circle",
            size=10,
            color=community_label,
            colorscale=["lightgreen", "magenta", "red"],
            line=dict(color="black", width=0.5),
        ),
        text=[
            f"Node {i}: {club_labels[i]}" for i in range(Num_nodes)
        ],  # Tooltip with node info
        hoverinfo="text",
    )

    # we need to set the axis for the plot
    axis = dict(
        showbackground=False,
        showline=False,
        zeroline=False,
        showgrid=False,
        showticklabels=False,
        title="",
    )

    # Create the layout for the figure
    fig = go.Figure(data=[trace_edges, trace_nodes])
    fig.update_layout(
        title="Mergers and Acquisitions",
        paper_bgcolor="rgba(0, 0, 0, 0)",  # Transparent background
        plot_bgcolor="rgba(0, 0, 0, 0)",  # Transparent plot area
        showlegend=False,
        width=650,
        height=625,
        scene=dict(
            xaxis=dict(axis),
            yaxis=dict(axis),
            zaxis=dict(axis),
        ),
        margin=dict(t=100),
        hovermode="closest",
    )

    return fig
