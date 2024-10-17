import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
from utils.data_loader import calculate_monthly_returns
from utils.graphs import gdp_per_state, plot_heatmap_monthly_changes
from utils.static_info import top_tickers

dash.register_page(__name__, path="/", redirect_from=["/home"], title="Home")

# Load the data
monthly_changes = calculate_monthly_returns(top_tickers, provider="yfinance")

# Create the heatmap
fig = plot_heatmap_monthly_changes(monthly_changes)

# Create state maps
map_fig = gdp_per_state()

layout = html.Div(
    className="main-container",
    children=[
        html.Div(
            className="landing-container",
            children=[
                html.P("AlphaEdge", className="landing-title"),
                html.P(
                    "Empowering you with data-driven market insights.",
                    className="landing-slogan",
                ),
                html.Div(className="scroll-indicator"),  # Vertical line component
            ],
        ),
        html.Hr(className="custom-divider"),
        html.H2("US Market Analysis"),
        # Detailed US Market Analysis Report
        html.Div(
            [
                html.H3(
                    "Heatmap Analysis of Top 20 U.S. Companies: Percentage of Return"
                ),
                html.P(
                    "The heatmap below visually represents the percentage of return for the top 20 U.S. companies, "
                    "with colors ranging from red to blue. This color gradient effectively communicates performance levels, "
                    "allowing for quick identification of high and low performers.",
                    className="text-block",  # Apply the text block class
                ),
                # --- Heatmap graph
                dcc.Graph(figure=fig),  # Add the heatmap to the layout
                # --- Map graph
                dcc.Graph(
                    figure=gdp_per_state(),
                    id="gdp-choropleth",
                    config={"displayModeBar": False},
                ),  # GDP map
                # Interval component to trigger animation
                dcc.Interval(
                    id="interval-component", interval=2000, n_intervals=0
                ),  # Adjust the interval as needed
                html.H3("Understanding Percentage of Return"),
                html.P(
                    "The percentage of return is a key financial metric that indicates the change in value of an investment over a specified period. "
                    "It is calculated using the following formula:"
                ),
                html.Div(
                    children=[
                        dcc.Markdown(
                            r"$\text{Percentage of Return} = \frac{(P_f - P_i)}{P_i} \times 100$",
                            mathjax=True,
                        ),
                        dcc.Markdown(
                            "Where: "
                            " $P_f$ = Final price of the investment (price at the end of the period), "
                            " $P_i$ = Initial price of the investment (price at the beginning of the period).",
                            mathjax=True,
                        ),
                    ],
                ),
                html.H3("Heatmap Color Gradient"),
                html.P(
                    "The heatmap utilizes a color gradient to convey the performance of each company:"
                ),
                html.Ul(
                    [
                        html.Li(
                            "Red Colors: Indicate negative returns, suggesting a decline in value. The deeper the shade of red, the larger the loss."
                        ),
                        html.Li(
                            "Blue Colors: Represent positive returns, indicating growth. Darker blue shades signify higher returns."
                        ),
                    ]
                ),
                html.H3("Methodology for Data Collection and Analysis"),
                html.P("To create the heatmap, the following steps were undertaken:"),
                html.Ul(
                    [
                        html.Li(
                            "Data Collection: Historical price data for the top 20 U.S. companies was gathered from reliable financial sources."
                        ),
                        html.Li(
                            "Calculation of Returns: The percentage of return for each company was calculated using the provided formula."
                        ),
                        html.Li(
                            "Heatmap Generation: A visualization library was used to create the heatmap, applying the color gradient based on the calculated returns."
                        ),
                    ]
                ),
                html.H3("Data Analysis from the Heatmap"),
                html.P("Analyzing the heatmap reveals valuable insights:"),
                html.Ul(
                    [
                        html.Li(
                            "High Performers: Companies in dark blue indicate significant positive returns, suggesting strong performance and favorable market conditions."
                        ),
                        html.Li(
                            "Underperformers: Companies in dark red highlight substantial declines, indicating potential challenges such as increased competition or declining demand."
                        ),
                        html.Li(
                            "Overall Trends: The heatmap allows stakeholders to quickly identify sectors performing well or poorly, guiding investment strategies."
                        ),
                    ]
                ),
                html.H3("Conclusion"),
                html.P(
                    "The heatmap serves as an essential tool for visualizing the percentage of return for the top 20 U.S. companies, providing impactful insights into market performance. "
                    "By understanding the percentage of return calculation and interpreting the color-coded data, investors can make informed decisions based on current market dynamics."
                ),
                # Adding some additional content for scrolling
                html.Div("Additional content goes here...", style={"height": "1500px"}),
            ]
        ),
    ],
)


# Callback to trigger the animation
@callback(
    Output("gdp-choropleth", "figure"), [Input("interval-component", "n_intervals")]
)
def update_gdp_map(n):
    # Calculate the year based on n_intervals
    year = 2010 + (n % 10)  # Loop through 2010-2019
    # Create the GDP figure
    fig = gdp_per_state()  # Get the initial figure
    fig.update_layout(title_text=f"USA GDP in {year}")  # Update the title
    return fig
