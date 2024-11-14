import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
from utils.data_loader import calculate_monthly_returns, load_state_gdp
from utils.graphs import (
    gdp_per_state,
    create_pyvis_network_graph,
    plot_heatmap_monthly_changes,
    plot_top_growing_companies,
    num_tech_companies,
)
import pickle
import networkx as nx
from utils.static_info import top_tickers
import pandas as pd
import plotly.graph_objects as go

dash.register_page(__name__, path="/", redirect_from=["/home"], title="Home")

# Load the data
monthly_changes = calculate_monthly_returns(top_tickers, provider="yfinance")
state_gdp = load_state_gdp()

# Load the graph from a file
with open("./graph_objs/company_graph.pkl", "rb") as f:
    G = pickle.load(f)

# Create a color map for industries globally
unique_industries = set(nx.get_node_attributes(G, "Industry").values())
color_scale = px.colors.qualitative.Plotly
industry_color_map = {
    industry: color_scale[i % len(color_scale)]
    for i, industry in enumerate(unique_industries)
}

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
        # Title Section
        html.Div(
            className="title-container",
            children=[
                html.H1("So what about USA", className="title-line"),
                html.H1("market analysis?", className="title-line"),
            ],
        ),
        # Diagonal background below the title
        html.Div(className="diagonal-background"),
        # Detailed US Market Analysis Report
        html.Div(
            [
                html.P(
                    [
                        "Market analysis is the process of assessing the dynamics of a market within a particular industry. It involves gathering and evaluating data to understand factors such as market size, trends, customer demographics, competition, and economic conditions. The goal of market analysis is to ",
                        html.Span("provide insights", className="highlighted-text"),
                        " that help businesses make informed decisions regarding their products or services, target audience, pricing strategies, and overall market positioning.",
                    ]
                ),
                # --- Heatmap graph
                html.H3("State GDP year by year"),
                html.P(
                    [
                        "Analyzing state GDP is crucial for market analysis because it provides insights into the economic health, consumer spending power, and industry-specific opportunities of a region. Higher GDP often indicates stronger economies, which means ",
                        html.Span("increased demand", className="highlighted-text"),
                        " for products and services. It helps businesses assess market potential, identify competitive landscapes, and make informed decisions on pricing, investment, and expansion. Additionally, it aids in risk assessment by highlighting potential economic risks and opportunities for ",
                        html.Span(
                            "government incentives", className="highlighted-text"
                        ),
                        ".",
                    ]
                ),
                # --- Map graph
                dcc.Graph(
                    figure=gdp_per_state(state_gdp, 2000),
                    id="gdp-choropleth",
                ),  # GDP map
                # Interval component to trigger animation
                # Interval component to trigger updates
                dcc.Interval(
                    id="interval-component",
                    interval=1000,  # Update every second (1000 milliseconds)
                    n_intervals=0,  # Start at 0
                ),
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
                html.P(
                    "We can use a heatmap utilizes a color gradient to convey the performance of each company:"
                ),
                html.Ul(
                    [
                        html.Li(
                            "Red Colors: Indicate negative returns, suggesting a decline in value. The deeper the shade of red, the larger the loss."
                        ),
                        html.Li(
                            "Blue Colors: Represent positive returns, indicating growth. Darker blue shades signify higher returns."
                        ),
                    ],
                    className="aligned-list",  # Add a custom class to control the alignment
                ),
                dcc.Graph(
                    figure=plot_heatmap_monthly_changes(monthly_changes)
                ),  # Add the heatmap to the layout
                html.H3(
                    "Importance of Analyzing Population Statistics in Each City and State"
                ),
                html.P(
                    [
                        "Analyzing population statistics in each city and state is crucial for understanding the drivers of economic growth and regional development. A larger population often signals a higher demand for goods, services, and housing, contributing to a more ",
                        html.Span("dynamic economy", className="highlighted-text"),
                        ". This, in turn, encourages greater ",
                        html.Span("business investment", className="highlighted-text"),
                        ", job creation, and infrastructure development, fueling innovation and expanding the local market.",
                        html.Br(),
                        html.Br(),
                        "Population data also enables businesses and governments to make informed decisions regarding resource allocation, public services, and urban planning. Regions experiencing population growth may require increased investment in education, healthcare, and transportation, while areas with declining populations may face economic stagnation or require targeted revitalization efforts.",
                        html.Br(),
                        html.Br(),
                        "Moreover, understanding the demographic makeup—such as age, income levels, and education—of different regions provides insights into consumer preferences, workforce skills, and economic potential. Businesses can leverage this data to tailor their products and services to meet local demand, while policymakers can use it to promote sustainable development and address regional disparities.",
                        html.Br(),
                        html.Br(),
                        "In summary, analyzing population statistics plays a fundamental role in shaping economic strategies, fostering growth, and ensuring that cities and states are equipped to meet the challenges and opportunities presented by changing demographic trends.",
                    ]
                ),
                dcc.Graph(
                    figure=plot_top_growing_companies()
                ),  # Add the heatmap to the layout
                html.H3(
                    "Importance of Analyzing the Number of Tech Companies per State"
                ),
                html.P(
                    [
                        "Analyzing the number of tech companies per state is crucial for understanding the evolving landscape of the technology sector in the U.S. Over the last 20 years, there has been a significant increase in the number of tech startups and established firms across various states, reflecting a shift in ",
                        html.Span("capital investment", className="highlighted-text"),
                        " and entrepreneurial activity. This growth suggests that regions are becoming more competitive in attracting technology talent and resources.",
                        html.Br(),
                        html.Br(),
                        "As states like California and New York have traditionally dominated the tech scene, emerging tech hubs in states such as Texas, Washington, and Florida have gained prominence. This trend indicates a broader distribution of tech companies, leading to ",
                        html.Span(
                            "economic diversification", className="highlighted-text"
                        ),
                        " and reduced reliance on a single market. Businesses are increasingly seeking opportunities in these new markets, driving innovation and creating job opportunities.",
                        html.Br(),
                        html.Br(),
                        "Furthermore, the changing dynamics of tech companies across states influence investment patterns and the allocation of resources. Regions with a high concentration of tech companies benefit from collaboration, knowledge sharing, and a skilled workforce. In contrast, states with fewer tech companies may miss out on these advantages, impacting their growth potential. Understanding these trends is essential for businesses looking to navigate the competitive landscape and capitalize on emerging opportunities in the tech sector.",
                    ]
                ),
                dcc.Graph(
                    figure=num_tech_companies()
                ),  # Add the graph to visualize tech company growth
                html.H3("Importance of Analyzing Corporate Acquisitions"),
                html.P(
                    [
                        "Analyzing corporate acquisitions, particularly in the technology sector, is crucial for understanding the dynamics of ",
                        html.Span("market power", className="highlighted-text"),
                        " and ",
                        html.Span("innovation", className="highlighted-text"),
                        ". Over the past two decades, major tech companies have aggressively expanded their portfolios by acquiring smaller firms, leading to significant shifts in competitive landscapes.",
                        html.Br(),
                        html.Br(),
                        "For instance, acquisitions such as Adobe's purchase of Figma illustrate how larger companies can enhance their capabilities and diversify their offerings. These acquisitions are not merely transactions; they signify ",
                        html.Span("strategic decisions", className="highlighted-text"),
                        " that reshape industries and influence technological advancement. By examining these relationships, we can identify patterns that reveal how established companies leverage their resources to fuel growth and ",
                        html.Span("innovation", className="highlighted-text"),
                        ".",
                        html.Br(),
                        html.Br(),
                        "Moreover, the parent-child relationships formed through acquisitions provide insights into the concentration of resources and talent within the tech ecosystem. Understanding which companies dominate this landscape helps in identifying emerging trends, potential market disruptions, and investment opportunities. Visualizing these relationships in a graph format allows stakeholders to analyze connections, dependencies, and the overall structure of the tech market.",
                        html.Br(),
                        html.Br(),
                        "In addition, detailed analyses of acquisition data can uncover the motivations behind these transactions. Are they driven by the desire to acquire ",
                        html.Span(
                            "cutting-edge technology", className="highlighted-text"
                        ),
                        ", access to new markets, or talent acquisition? By studying these aspects, businesses and investors can make informed decisions based on the evolving landscape of corporate strategies.",
                        html.Br(),
                        html.Br(),
                        "Ultimately, a comprehensive understanding of tech company acquisitions and their implications is essential for navigating the competitive landscape. As the technology sector continues to evolve, staying informed about these changes will empower organizations to capitalize on emerging opportunities and mitigate potential risks.",
                    ]
                ),
                html.Div(
                    [
                        html.Div(
                            style={
                                "display": "flex",
                                "justify-content": "center",
                                "margin-top": "20px",
                                "margin-bottom": "20px",
                            },
                            children=[
                                dcc.Dropdown(
                                    id="company-dropdown",
                                    options=[
                                        {
                                            "label": "All Companies",
                                            "value": "All Companies",
                                        }
                                    ]
                                    + [
                                        {"label": node, "value": node}
                                        for node in G.nodes()
                                    ],
                                    value="All Companies",
                                    style={
                                        "width": "50%",
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            id="company-graph-iframe"
                        ),  # Placeholder for the Pyvis graph
                    ]
                ),
                html.Br(),
                html.H3("Conclusion"),
                html.P(
                    [
                        "In conclusion, the comprehensive market analysis presented in this report highlights critical insights into the ",
                        html.Span("economic landscape", className="highlighted-text"),
                        " of the United States. By evaluating various metrics such as GDP per state, percentage of return, and the number of companies operating in different regions, we can better understand the underlying dynamics shaping the market.",
                        html.Br(),
                        html.Br(),
                        "The analysis of state GDP serves as a vital indicator of economic health, revealing how regional strengths can influence business decisions and investment strategies. As we've seen, states with higher GDP figures not only reflect robust ",
                        html.Span(
                            "consumer spending power", className="highlighted-text"
                        ),
                        " but also present abundant opportunities for growth and expansion. This information is invaluable for companies looking to navigate potential risks and capitalize on emerging market trends.",
                        html.Br(),
                        html.Br(),
                        "Furthermore, our examination of the percentage of return offers a clearer picture of individual company performance within the broader market context. The heatmap visualization effectively illustrates the varying returns across companies, enabling stakeholders to identify areas of both risk and opportunity. Understanding these ",
                        html.Span("performance metrics", className="highlighted-text"),
                        " is essential for investors and decision-makers who wish to optimize their portfolios and investments.",
                        html.Br(),
                        html.Br(),
                        "Lastly, analyzing the number of companies operating within each state provides insight into the competitive landscape. A thriving business ecosystem not only fosters innovation and collaboration but also enhances regional ",
                        html.Span("economic resilience", className="highlighted-text"),
                        ". The data suggests that states with a higher concentration of companies may experience accelerated growth and development, ultimately benefiting the local economy.",
                        html.Br(),
                        html.Br(),
                        "Overall, this analysis underscores the importance of ",
                        html.Span("data-driven insights", className="highlighted-text"),
                        " in making informed business decisions. By leveraging the visualizations and metrics provided, stakeholders can better understand market dynamics, identify trends, and formulate strategies that align with the evolving economic landscape.",
                    ]
                ),
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
    year = 2000 + (n % 24)  # Loop through 2000-2024
    # Create the GDP figure
    fig = gdp_per_state(state_gdp, year)  # Get the initial figure
    fig.update_layout(title_text=f"USA GDP in {year}")  # Update the title
    return fig


@callback(
    Output("company-graph-iframe", "children"),
    Input("company-dropdown", "value"),
)
def update_graphs_and_info(selected_company):
    graph_html = create_pyvis_network_graph(G, selected_company)  # Create Pyvis graph
    graph_iframe = html.Iframe(
        id="company-graph-iframe",  # Ensure this is the correct ID
        srcDoc=graph_html,  # Your graph data
        height="600px",
        width="800px",
        style={
            "border": "none",  # Remove border
            "backgroundColor": "rgba(255, 255, 255, 0)",  # Transparent background
            "display": "block",  # Make it a block element
            "margin": "auto",  # Center the iframe
        },
    )

    return (graph_iframe,)  # Return the iframe with the Pyvis graph
