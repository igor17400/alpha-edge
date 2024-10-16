import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
from utils.data_loader import calculate_monthly_returns
from utils.graphs import plot_heatmap_monthly_changes
from utils.static_info import top_tickers

dash.register_page(__name__, path="/", redirect_from=["/home"], title="Home")

# Load the data

monthly_changes = calculate_monthly_returns(top_tickers, provider="yfinance")

# Create the heatmap
fig = plot_heatmap_monthly_changes(monthly_changes)

layout = html.Div(
    className="main-container",
    # style={
    #     "height": "100vh",  # Full height of the viewport
    #     "overflowY": "scroll",  # Enable vertical scrolling
    #     "padding": "20px",  # Optional: add padding
    #     "boxSizing": "border-box",  # Ensure padding is included in height
    # },
    children=[
        html.H1(
            [
                "Welcome to the ",
                html.Span("AlphaEdge", className="highlighted-text"),
            ]
        ),
        html.P("Empowering you with data-driven market insights."),
        dcc.Graph(figure=fig),  # Add the heatmap to the layout
        # You can add more content here to ensure scrolling works
        html.Div(
            "Additional content goes here...", style={"height": "1500px"}
        ),  # Example content for scrolling
    ],
)


@callback(Output("content", "children"), Input("radios", "value"))
def home_radios(value):
    return f"You have selected {value}"
