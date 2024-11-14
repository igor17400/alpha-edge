import pandas as pd
import os
from urllib.request import urlopen
import json
import certifi

from dotenv import load_dotenv
load_dotenv("../.env")
API_KEY = os.getenv("FMP_API_KEY")

# Constants
BASE_URL = "https://financialmodelingprep.com/api/v4/mergers-acquisitions-rss-feed"
TOTAL_PAGES = 45
data = []

def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

# Fetch data from the API
for page in range(1, TOTAL_PAGES + 1):
    url = f"{BASE_URL}?page={page}&apikey={API_KEY}"
    data.extend(get_jsonparsed_data(url))

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("../datasets/mergers_acquisitions_data.csv", index=False)
print("Data saved to mergers_acquisitions_data.csv")
