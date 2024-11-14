from urllib.request import urlopen

import certifi
import json
from dotenv import load_dotenv
import os

load_dotenv()
fmp_api_key = os.getenv('FMP_API_KEY')

def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)


url = f"https://financialmodelingprep.com/api/v4/mergers-acquisitions-rss-feed?page=0&apikey={fmp_api_key}"
print(get_jsonparsed_data(url))

# url = (f"https://financialmodelingprep.com/api/v4/search/isin?isin=US0378331005&apikey={fmp_api_key}")
# print(get_jsonparsed_data(url))
