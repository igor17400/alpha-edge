GENERATE_SUBQUESTION_SYSTEM_PROMPT_TEMPLATE = """\

Don't generate any comments, or "Notes". Return only the JSON with Markdown.

You are a world-class state-of-the-art agent called OpenBB Agent.

Your purpose is to help answer a complex user question by generating a list of subquestions (but only if necessary).

You must also specify the dependencies between subquestions, since sometimes one subquestion will require the outcome of another in order to fully answer.

## Guidelines
* Don't try to be too clever
* Assume Subquestions are answerable by a downstream agent using tools to lookup the information.
* You must generate at least 1 subquestion.
* Generate only the subquestions required to answer the user's question
* Generate as few subquestions as possible required to answer the user's question
* A subquestion may not depend on a subquestion that proceeds it (i.e. comes after it.)
* Assume tools can be used to look-up the answer to the subquestions (e.g., for market cap, just create a subquestion asking for the market cap rather than for the components to calculate it.)

### Example output
```json
{{"subquestions": [
    {{
        "id": 1,
        "question": "What are the latest financial statements of AMZN?",
        "depends_on": []
    }},
    {{
        "id": 2,
        "question": "What is the most recent revenue and profit margin of AMZN?",
        "depends_on": []
    }},
    {{
        "id": 3,
        "question": "What is the current price to earnings (P/E) ratio of AMZN?",
        "depends_on": []
    }},
    {{
        "id": 4,
        "question": "Who are the peers of AMZN?",
        "depends_on": []
    }},
    {{
        "id": 5,
        "question": "Which of AMZN's peers have the largest market cap?",
        "depends_on": [4]
    }}
]}}
"""

from magentic.chat_model.retry_chat_model import RetryChatModel
from pydantic import BaseModel, Field, ValidationError
from typing import List
from magentic import (
    OpenaiChatModel,
    UserMessage,
    chatprompt,
    SystemMessage,
    prompt_chain,
)
import logging
import json
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Read the existing CSV file
df = pd.read_csv('./datasets/us_market_data.csv')

# Create a new DataFrame with only the 'symbol' and 'name' columns
ticker_to_name_df = df[['symbol', 'name']]

# Define a system prompt for the ollama model
GENERATE_TICKER_TO_NAME_PROMPT_TEMPLATE = """\
You are a data processing agent. Your task is to map stock tickers to company names from a given dataset.
Don't return any comments, or "Notes". Return only the company name.
"""

@chatprompt(
    SystemMessage(GENERATE_TICKER_TO_NAME_PROMPT_TEMPLATE),
    UserMessage("# Data processing task\nTicker: {ticker}, Name: {name}"),
    model=OpenaiChatModel(
        model="llama3.1:latest",
        api_key="ollama",
        base_url="http://localhost:11434/v1/",
    ),
)
def process_ticker_to_name(ticker: str, name: str) -> str: ...

# Initialize an empty dictionary to store the results
ticker_to_name_dict = {}

# Iterate over each row in the DataFrame
for index, row in ticker_to_name_df.iterrows():
    ticker = row['symbol']
    name = row['name']
    # Process each ticker and name using the ollama model
    response = process_ticker_to_name(ticker=ticker, name=name)
    # Store the result in the dictionary
    ticker_to_name_dict[ticker] = response

# Convert the dictionary to a DataFrame
processed_df = pd.DataFrame(list(ticker_to_name_dict.items()), columns=['symbol', 'name'])

# Save the processed DataFrame to a CSV file
processed_df.to_csv('./datasets/ticker_to_name.csv', index=False)

# Log the completion
logger.info("Created ticker_to_name.csv with ticker to company name mapping.")
