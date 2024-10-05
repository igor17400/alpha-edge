from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from layout import create_layout
from callbacks import register_callbacks
import config
from openbb import obb

# Create the Dash app
app = Dash(__name__)
server = app.server  # Expose the Flask server


# Function to check API credentials
def verify_api_credentials(token):
    """Attempts to log in and verify if OpenBB API credentials are valid."""
    try:
        obb.account.login(pat=token)
        if obb.user.credentials:
            obb.user.preferences.output_type = "dataframe"
            return "success"
        else:
            return "fail"
    except Exception as e:
        return f"error: {str(e)}"


# Initial layout with placeholders for IDs
# Initial layout with placeholders for IDs
app.layout = html.Div(
    [
        html.Div(
            dcc.Loading(
                id="loading-screen",
                type="default",
                children=[html.Div(id="loading-output")],
            ),
            style={
                "position": "absolute",
                "top": "50%",
                "left": "50%",
                "transform": "translate(-50%, -50%)",
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
                "height": "100vh",
            },
        ),
        # Placeholder Div for content (empty until API verification completes)
        html.Div(id="app-content"),
        # Placeholders for all the graph components used in callbacks
        dcc.Graph(id="market-overview-graph", style={"display": "none"}),
        dcc.Dropdown(id="stock-selector", style={"display": "none"}),
        dcc.Graph(id="stock-comparison-graph", style={"display": "none"}),
    ],
    style={"position": "relative", "height": "100vh"},
)


@app.callback(
    [
        Output("loading-output", "children"),
        Output("app-content", "children"),
        Output("market-overview-graph", "style"),
        Output("stock-selector", "style"),
        Output("stock-comparison-graph", "style"),
    ],
    Input("loading-screen", "children"),
)
def load_app_content(dummy):
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


# Register callbacks
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
