import os
import dash
from dash import Dash, html, dcc
from flask import Flask
import dash_bootstrap_components as dbc

from utils.settings import APP_HOST, APP_PORT, APP_DEBUG, DEV_TOOLS_PROPS_CHECK
from components import navbar, footer

# Create Dash app
server = Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    use_pages=True,  # turn on Dash pages
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
    ],  # fetch the proper css items we want
    meta_tags=[
        {  # check if device is a mobile device. This is a must if you do any mobile styling
            "name": "viewport",
            "content": "width=device-width, initial-scale=1",
        }
    ],
    suppress_callback_exceptions=True,
    title="AlphaEdge",
)

server.config.update(SECRET_KEY=os.getenv("SECRET_KEY"))


def serve_layout():
    """Define the layout of the application"""
    return html.Div(
        [
            navbar,
            dbc.Container(dash.page_container, class_name="my-2"),
            footer,
        ]
    )


app.layout = serve_layout  # set the layout to the serve_layout function
server = app.server  # the server is needed to deploy the application

if __name__ == "__main__":
    app.run_server(
        host=APP_HOST,
        port=APP_PORT,
        debug=APP_DEBUG,
        dev_tools_props_check=DEV_TOOLS_PROPS_CHECK,
    )
