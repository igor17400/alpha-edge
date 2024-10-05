from dash import html, dcc


def create_layout():
    """
    Create the layout for the Dash app.
    
    :return: Dash layout.
    """
    return html.Div(
        [
            html.H1("Brazilian Stock Market Analysis"),
            dcc.Tabs(
                [
                    dcc.Tab(
                        label="Market Overview",
                        children=[
                            html.Div(
                                [
                                    html.H2("Market Overview"),
                                    dcc.Graph(id="market-overview-graph"),
                                ]
                            )
                        ],
                    ),
                    dcc.Tab(
                        label="Stock Comparison",
                        children=[
                            html.Div(
                                [
                                    html.H2("Stock Comparison"),
                                    dcc.Dropdown(
                                        id="stock-selector",
                                        options=[
                                            {"label": "PETR4", "value": "PETR4"},
                                            {"label": "VALE3", "value": "VALE3"},
                                            {"label": "ITUB4", "value": "ITUB4"},
                                        ],
                                        multi=True,
                                        value=["PETR4"],
                                    ),
                                    dcc.DatePickerRange(
                                        id="date-range-picker",
                                        start_date="2022-01-01",
                                        end_date="2023-01-01",
                                    ),
                                    dcc.Dropdown(
                                        id="data-provider",
                                        options=[
                                            {
                                                "label": "Yahoo Finance",
                                                "value": "yahoo",
                                            },
                                            {"label": "Alpaca", "value": "alpaca"},
                                        ],
                                        value="yahoo",
                                        placeholder="Select data provider",
                                    ),
                                    dcc.Graph(id="stock-comparison-graph"),
                                ]
                            )
                        ],
                    ),
                ]
            ),
        ]
    )
