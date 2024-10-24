# Import the required packages
import networkx as nx
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import plotly.express as px
from scipy.interpolate import griddata
from scipy.spatial import Voronoi
from scipy.spatial import cKDTree


def load_company_data():
    # Load the CSV file
    df = pd.read_csv("./datasets/Acquisitions.csv")

    # Rename columns to match the expected structure
    df = df.rename(
        columns={
            "Acquired Company": "Company",
            "Acquiring Company": "Parent",
            "Price": "Market Cap",
        }
    )

    # Add additional columns if needed
    industries = ["Technology", "Healthcare", "Sales", "Banking", "Retail"]
    df["Industry"] = df.apply(
        lambda x: np.random.choice(industries), axis=1
    )  # Randomly a
    df["Location"] = "USA"  # Placeholder, update with actual data if available
    df["City"] = "Unknown"  # Placeholder, update with actual data if available

    return df


# Initialize the Dash app
app = Dash(__name__)

# Load data and create graph
df = load_company_data()

# Create a color map for industries globally
unique_industries = df["Industry"].unique()
color_scale = px.colors.qualitative.Plotly
industry_color_map = {
    industry: color_scale[i % len(color_scale)]
    for i, industry in enumerate(unique_industries)
}


# Create graph from company data
def create_company_graph(df):
    G = nx.DiGraph()

    # Add nodes for acquired companies
    for _, row in df.iterrows():
        G.add_node(
            row["Company"],
            Industry=row.get("Industry", "Unknown"),
            Market_Cap=row.get("Market Cap", 0),
            Year_Acquired=row.get("Year Acquired", 0),
            Deal_Date=row.get("Deal Date", 0),
        )
        if row["Parent"]:
            if row["Parent"] not in G:
                G.add_node(
                    row["Parent"],
                    Industry=row.get("Industry", "Unknown"),
                    Market_Cap=0,
                    Year_Acquired=0,
                    Deal_Date=0,
                )
            G.add_edge(row["Parent"], row["Company"])

    return G


G = create_company_graph(df)


# Create the 3D network graph
def create_3d_network_graph(G, df, selected_company):
    # Set a fixed seed for reproducibility
    np.random.seed(42)

    # Create a color map for industries
    unique_industries = df["Industry"].unique()
    color_scale = px.colors.qualitative.Plotly
    industry_color_map = {
        industry: color_scale[i % len(color_scale)]
        for i, industry in enumerate(unique_industries)
    }

    # Get the subgraph for the selected company or use the full graph
    if selected_company == "All Companies":
        subgraph = G
    elif selected_company in G:
        subgraph = nx.ego_graph(G, selected_company, radius=1, undirected=True)
    else:
        subgraph = G  # Fallback to full graph if selection is invalid

    # Create positions for each industry sector
    n_industries = len(unique_industries)
    industry_positions = {}
    for i, industry in enumerate(unique_industries):
        theta = 2 * np.pi * i / n_industries
        r = 1.0  # Fixed radius for each industry
        industry_positions[industry] = (r * np.cos(theta), r * np.sin(theta), 0)

    # Position nodes within their industry sector
    pos = {}
    for node in subgraph.nodes():
        industry = G.nodes[node]["Industry"]
        base_x, base_y, base_z = industry_positions[industry]
        offset_x = np.random.normal(0, 0.1)
        offset_y = np.random.normal(0, 0.1)
        offset_z = np.random.normal(0, 0.1)
        pos[node] = (base_x + offset_x, base_y + offset_y, base_z + offset_z)

    edge_trace = go.Scatter3d(
        x=[],
        y=[],
        z=[],
        line=dict(width=1, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    for edge in subgraph.edges():
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        edge_trace["x"] += (x0, x1, None)
        edge_trace["y"] += (y0, y1, None)
        edge_trace["z"] += (z0, z1, None)

    node_trace = go.Scatter3d(
        x=[],
        y=[],
        z=[],
        mode="markers",
        hoverinfo="text",
        marker=dict(showscale=False, color=[], size=[], symbol=[], line_width=2),
    )

    # Normalize market cap for node size
    max_market_cap = df["Market Cap"].max()
    min_market_cap = df["Market Cap"].min()

    for node in subgraph.nodes():
        x, y, z = pos[node]
        node_trace["x"] += (x,)
        node_trace["y"] += (y,)
        node_trace["z"] += (z,)
        industry = G.nodes[node]["Industry"]
        node_trace["marker"]["color"] += (industry_color_map[industry],)
        market_cap = G.nodes[node]["Market_Cap"]
        node_size = (
            10
            + ((market_cap - min_market_cap) / (max_market_cap - min_market_cap)) * 20
        )
        node_trace["marker"]["size"] += (node_size,)
        # Set shape based on whether it's a parent or child company
        is_parent = any(df["Parent"] == node)
        node_trace["marker"]["symbol"] += ("square" if is_parent else "circle",)

    node_text = []
    for node in subgraph.nodes():
        parent = df[df["Company"] == node]["Parent"].values[0]
        parent_info = f"Parent: {parent}" if parent else "Parent: None"
        node_text.append(
            f"Company: {node}<br>Industry: {G.nodes[node]['Industry']}<br>Market Cap: ${G.nodes[node]['Market_Cap']} billion<br>{parent_info}"
        )

    node_trace.text = node_text

    title = (
        "All Company Relationships"
        if selected_company == "All Companies"
        else f"Company Relationships for {selected_company}"
    )
    layout = go.Layout(
        title=title,
        titlefont_size=16,
        showlegend=False,
        hovermode="closest",
        margin=dict(b=20, l=5, r=5, t=40),
        scene=dict(
            xaxis=dict(
                showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title="",
            ),
            yaxis=dict(
                showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title="",
            ),
            zaxis=dict(
                showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title="",
            ),
        ),
        height=600,
        width=800,
    )

    fig = go.Figure(data=[edge_trace, node_trace], layout=layout)
    return fig


# Define the layout of the Dash app
app.layout = html.Div(
    [
        dcc.Dropdown(
            id="company-dropdown",
            options=[{"label": "All Companies", "value": "All Companies"}]
            + [{"label": company, "value": company} for company in df["Company"]],
            value="All Companies",
            style={"width": "50%"},
        ),
        dcc.Checklist(
            id="include-parent-checkbox",
            options=[{"label": "Include Parent Company", "value": "include_parent"}],
            value=[],  # Default to exclude parent
            style={"margin": "10px 0"},
        ),
        dcc.Graph(id="company-graph-3d"),
        html.Div(id="company-info"),
        dcc.Graph(id="company-treemap"),  # Add a new Graph for the treemap
        dcc.Graph(id="company-geo-map"),  # Add a new Graph for the geographic map
    ]
)


@callback(
    Output("company-graph-3d", "figure"),
    Output("company-info", "children"),
    Output("company-treemap", "figure"),  # Output for the treemap
    Output("company-geo-map", "figure"),  # Output for the geographic map
    Input("company-dropdown", "value"),
    Input("include-parent-checkbox", "value"),
)
def update_graphs_and_info(selected_company, include_parent):
    fig_3d = create_3d_network_graph(G, df, selected_company)
    fig_treemap = go.Figure()
    fig_geo = go.Figure()

    if selected_company and selected_company != "All Companies":
        # Treemap logic
        child_companies = df[df["Parent"] == selected_company]
        data = child_companies.copy()
        if "include_parent" in include_parent:
            parent_company_data = df[df["Company"] == selected_company]
            data = pd.concat([parent_company_data, data])
        data["Label"] = (
            data["Company"]
            + "<br>"
            + data["Market Cap"].apply(lambda x: f"${x:,.2f} billion")
        )
        fig_treemap = px.treemap(
            data,
            path=["Label"],
            values="Market Cap",
            color="Industry",
            color_discrete_map=industry_color_map,
            title=f'Market Capitalization of {selected_company} {"and its Child Companies" if "include_parent" in include_parent else "Child Companies Only"}',
        )
        fig_treemap.update_layout(width=1200, height=700)

        # Geographic map logic
        fig_geo = create_geo_map(df, selected_company)

    # Company info logic
    if selected_company == "All Companies":
        info = html.Div(
            [
                html.H3("All Companies Overview"),
                html.P(f"Total number of companies: {len(df)}"),
                html.P(f"Industries represented: {', '.join(df['Industry'].unique())}"),
                html.P(f"Total market cap: ${df['Market Cap'].sum()} billion"),
            ]
        )
    else:
        company_data = df[df["Company"] == selected_company].iloc[0]
        children = df[df["Parent"] == selected_company]["Company"].tolist()
        info = html.Div(
            [
                html.H3(f"Information for {selected_company}"),
                html.P(f"Industry: {company_data['Industry']}"),
                html.P(f"Market Cap: ${company_data['Market Cap']} billion"),
                html.P(f"Parent Company: {company_data['Parent'] or 'None'}"),
                html.P(
                    f"Child Companies: {', '.join(children) if children else 'None'}"
                ),
            ]
        )

    return (
        fig_3d,
        info,
        fig_treemap,
        fig_geo,
    )  # Return the treemap and geographic map figures


def create_geo_map(df, selected_company):
    # Filter data for child companies of the selected parent company
    child_companies = df[df["Parent"] == selected_company]

    # Include parent company if needed
    parent_company_data = df[df["Company"] == selected_company]
    data = pd.concat([parent_company_data, child_companies])

    # Create the map
    fig_geo = px.scatter_geo(
        data,
        locations="Location",  # Use country names
        locationmode="country names",
        size="Market Cap",  # Size of the marker based on market cap
        hover_name="Company",
        hover_data={"City": True},  # Include city in hover data
        title=f"Geographic Distribution of {selected_company} and its Child Companies",
        projection="natural earth",
    )

    fig_geo.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=500)

    return fig_geo


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8039)
