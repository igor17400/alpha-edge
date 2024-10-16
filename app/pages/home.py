# package imports
import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__, path="/", redirect_from=["/home"], title="Home")

layout = html.Div(
    className="main-container",
    children=[
        html.H1(
            [
                "Welcome to the ",
                html.Span("AlphaEdge", className="highlighted-text"),
            ]
        ),
        html.P(
            "Empowering you with data-driven market insights."
        ),
        html.Div(
            [
                html.A(
                    "Explore Stock Comparisons",
                    href="/complex",
                    style={"margin-right": "10px"},
                ),
                html.A("Visit Page 2", href="/page2"),
            ],
            style={"margin-bottom": "40px"},
        ),
        dcc.RadioItems(
            id="radios",
            options=[{"label": i, "value": i} for i in ["Orange", "Blue", "Red"]],
            value="Orange",
            style={"margin-bottom": "20px"},
        ),
        html.Div(id="content"),
    ],
)


@callback(Output("content", "children"), Input("radios", "value"))
def home_radios(value):
    return f"You have selected {value}"
