import dash
from dash import html, dcc, callback, Input, Output, State
import requests
import json
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
import os
import random

from utils.settings import FMP_API_KEY, APP_PORT

# Load environment variables from .env file
load_dotenv("../.env")

# Load API key from .env file
print("-------")
print(APP_PORT)
print(FMP_API_KEY)
print("-------")

# Initialize the Dash app
dash.register_page(__name__, path="/company-analysis", title="Company Analysis")

# Function to fetch top 20 companies from S&P 500 constituents
def fetch_top_companies():
    url = f"https://financialmodelingprep.com/api/v3/sp500_constituent?apikey={FMP_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    # Return the first 20 companies from the S&P 500
    return data[:20]  # Assuming the API returns a list of dictionaries

# Function to fetch detailed company information
def fetch_company_info(symbol):
    url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={FMP_API_KEY}"  # Use the loaded API key
    response = requests.get(url)
    return response.json()[0]  # Return the first company info

# Function to generate a random gradient color
def random_gradient():
    color1 = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    color2 = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    return f"linear-gradient(135deg, {color1}, {color2})"

# Fetch the top companies' data
top_companies = fetch_top_companies()  # Fetch detailed info for each symbol

# Layout for the company analysis page
layout = html.Div(
    className="company-analysis-container",
    children=[
        html.H1("S&P 500 Constituents", className="title"),
        dcc.Loading(  # Add loading component
            id="loading",
            type="default",  # You can change this to "circle", "dot", or "default"
            children=[
                html.Div(
                    className="company-cards",
                    children=[
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            style={
                                                "height": "150px",  # Set a fixed height for the gradient area
                                                "background": random_gradient(),  # Set random gradient background
                                                "borderRadius": "10px",  # Rounded corners
                                            },
                                        ),
                                        html.H4(company["symbol"], className="card-title"),  # Use symbol for the title
                                        html.P(f"Price: ${company.get('price', 'N/A')}", className="card-text"),  # Use get to avoid KeyError
                                        dbc.Button(
                                            "View Details",
                                            id={
                                                "type": "detail-button",
                                                "index": company["symbol"],
                                            },
                                            color="primary",
                                        ),
                                    ]
                                ),
                            ],
                            style={"width": "18rem", "margin": "10px"},
                        )
                        for company in top_companies
                    ],
                    style={"display": "flex", "flexWrap": "wrap", "justifyContent": "center"},
                ),
                html.Div(id="company-details", style={"marginTop": "20px"}),
            ],
        ),
        # Modal for displaying company details
        dbc.Modal(
            [
                dbc.ModalHeader(id="modal-header"),
                dbc.ModalBody(id="modal-body"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto")
                ),
            ],
            id="modal",
            size="lg",
        ),
    ],
)

# Callback to update company details when a card is clicked
@callback(
    Output("modal", "is_open"),
    Output("modal-header", "children"),
    Output("modal-body", "children"),
    Input({"type": "detail-button", "index": dash.dependencies.ALL}, "n_clicks"),
    Input("close", "n_clicks"),
    State("modal", "is_open"),
)
def display_company_details(n_clicks, close_click, is_open):
    ctx = dash.callback_context

    if ctx.triggered:
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if "detail-button" in triggered_id:  # If a detail button was clicked
            filtered_clicks = [click for click in n_clicks if click is not None]
            if not filtered_clicks:  # If no button has been clicked
                return False, "", ""

            index = filtered_clicks.index(max(filtered_clicks))  # Get the first button that was clicked
            symbol = top_companies[index]["symbol"]  # Get the corresponding symbol
            company_info = fetch_company_info(symbol)  # Fetch detailed info

            # Create the modal content
            modal_header = company_info["companyName"]
            modal_body = [
                html.Img(src=company_info["image"], style={"width": "100px", "height": "100px"}),
                html.P(f"CEO: {company_info['ceo']}"),
                html.P(f"Sector: {company_info['sector']}"),
                html.P(f"Description: {company_info['description']}"),
                html.P(f"Market Cap: ${company_info['mktCap']:,}"),
                html.P(f"Price: ${company_info['price']}"),
                html.P(f"Exchange: {company_info['exchange']}"),
                html.P(f"Website: {html.A(company_info['website'], href=company_info['website'], target='_blank')}")
            ]

            return True, modal_header, modal_body

        elif "close" in triggered_id:  # If the close button was clicked
            return not is_open, "", ""

    return is_open, "", ""  # Default return if no button was clicked
