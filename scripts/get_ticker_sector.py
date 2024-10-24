from magentic.chat_model.retry_chat_model import RetryChatModel
from pydantic import BaseModel, Field, ValidationError
from typing import List
from magentic import (
    OpenaiChatModel,
    UserMessage,
    chatprompt,
    SystemMessage,
)
import logging
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Read the existing CSV file
df = pd.read_csv('../datasets/us_market_data.csv')

# Create a new DataFrame with only the 'symbol' column
ticker_to_sector_df = df[['symbol']]

# Define a system prompt for the ollama model
GENERATE_TICKER_TO_SECTOR_PROMPT_TEMPLATE = """\
You are a data processing agent. Your task is to map stock tickers to their respective sectors from a given dataset.
Don't return any comments, or "Notes". Return only the sector.
"""

@chatprompt(
    SystemMessage(GENERATE_TICKER_TO_SECTOR_PROMPT_TEMPLATE),
    UserMessage("# Data processing task\nTicker: {ticker}"),
    model=OpenaiChatModel(
        model="llama3.1:latest",
        api_key="ollama",
        base_url="http://localhost:11434/v1/",
    ),
)
def process_ticker_to_sector(ticker: str) -> str: ...

# Initialize an empty dictionary to store the results
ticker_to_sector_dict = {}

# Iterate over each row in the DataFrame
for index, row in ticker_to_sector_df.iterrows():
    ticker = row['symbol']

    # Process each ticker using the ollama model to get the sector
    sector = process_ticker_to_sector(ticker=ticker)
    
    # Store the result in the dictionary
    ticker_to_sector_dict[ticker] = sector

# Convert the dictionary to a DataFrame
processed_df = pd.DataFrame(list(ticker_to_sector_dict.items()), columns=['symbol', 'sector'])

# Save the processed DataFrame to a CSV file
processed_df.to_csv('../datasets/ticker_to_sector.csv', index=False)

# Log the completion
logger.info("Created ticker_to_sector.csv with ticker to sector mapping.")
