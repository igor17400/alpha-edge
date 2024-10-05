from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

def register_callbacks(app):
    @app.callback(
        Output('market-overview-graph', 'figure'),
        Input('market-overview-graph', 'id')
    )
    def update_market_overview(dummy):
        # Placeholder data - replace with actual data loading
        df = pd.DataFrame({
            'Date': pd.date_range(start='2022-01-01', periods=100),
            'IBOVESPA': np.random.randint(100000, 120000, 100)
        })
        fig = px.line(df, x='Date', y='IBOVESPA', title='IBOVESPA Index')
        return fig

    @app.callback(
        Output('stock-comparison-graph', 'figure'),
        Input('stock-selector', 'value')
    )
    def update_stock_comparison(selected_stocks):
        # Placeholder data - replace with actual data loading
        df = pd.DataFrame({
            'Date': pd.date_range(start='2022-01-01', periods=100),
            'PETR4': np.random.randint(20, 30, 100),
            'VALE3': np.random.randint(70, 90, 100),
            'ITUB4': np.random.randint(20, 25, 100)
        })
        fig = px.line(df, x='Date', y=selected_stocks, title='Stock Price Comparison')
        return fig
