import os
from dotenv import load_dotenv

from typing import Literal
from IPython.display import display
from IPython.display import clear_output
import ipywidgets as widgets
import pandas as pd
from datetime import datetime
from plotly import graph_objects as go

from openbb import obb

# Load environment variables from .env file
load_dotenv()

openbb_token = os.getenv('OPENBB_TOKEN')

obb.account.login(pat=openbb_token)

# Verify that the credentials from Hub were loaded successfully.
print(obb.user.credentials)

# Set the output preference, if desired. The examples below use Pandas DataFrames.

obb.user.preferences.output_type = "dataframe"

symbol="AAPL"
options = obb.derivatives.options.chains(symbol, provider="yfinance")

# Prepare A View - Volume and Open Interest by Expiration or Strike

def filter_options_data(options, by: Literal["expiration", "strike"] = "expiration"):
    data = pd.DataFrame()
    data["Total Open Interest"] = options.groupby(by)["open_interest"].sum()
    data["Call Open Interest"] = options[options["option_type"] == "call"].groupby(by)["open_interest"].sum()
    data["Put Open Interest"] = options[options["option_type"] == "put"].groupby(by)["open_interest"].sum()
    data["Total Volume"] = options.groupby(by)["volume"].sum()
    data["Call Volume"] = options[options["option_type"] == "call"].groupby(by)["volume"].sum()
    data["Put Volume"] = options[options["option_type"] == "put"].groupby(by)["volume"].sum()

    return data

data = filter_options_data(options, "strike")


# Create a widget for selecting the data to display.

clear_output(wait = False)

data_choices = data.columns.tolist()
data_selection = widgets.Dropdown(
    options = data_choices,
    value = None,
)
output = widgets.Output()


def generate_figure(data, data_choice):
    data = data[data[data_choice].notnull()]
    fig = go.Figure()
    fig.add_bar(
        y = data[data_choice][data[data_choice] > 0].values,
        x = data[data_choice][data[data_choice] > 0].index,
        name = data_choice,
        marker = dict(color = "blue"),
    )
    fig.add_bar(
        y = data[data_choice][data[data_choice] < 0].values,
        x = data[data_choice][data[data_choice] < 0].index,
        name = data_choice,
        marker = dict(color = "red")
    )
    fig.update_xaxes(type="category")
    fig.update_traces(width=0.98, selector=dict(type="bar"))
    fig.update_layout(
        showlegend=False,
        width=1400,
        height=600,
        title = dict(
            text=f"{symbol} {data_choice.replace('_', ' ').title()}",
            xanchor = "center",
            x = 0.5,
            font = dict(size = 20)
        ),
        barmode="overlay",
        bargap=0,
        bargroupgap=0,
        yaxis=dict(
            ticklen=0,
            showgrid=True,
            tickfont=dict(size=14),
        ),
        xaxis=dict(
            showgrid=False,
            autorange=True,
            tickangle=90,
            tickfont=dict(size=11),
        ),
    )
    return fig

def on_value_change(change):
    clear_output(wait = True)
    display(data_selection)
    with output:
        data_selection.value

data_selection.observe(on_value_change, names="value")
display(data_selection)

# Select from the drop-down menu below.