# Import the required packages
import networkx as nx
import plotly.graph_objects as go
from dash import Dash, dcc, html

# Initialize the Dash app
app = Dash(__name__)

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

# Define the layout of the Dash app
app.layout = html.Div([dcc.Graph(figure=fig)])

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8039)
