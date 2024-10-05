import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
OPENBB_TOKEN = os.getenv('OPENBB_TOKEN')
DASH_APP_TITLE = os.getenv("DASH_APP_TITLE", "QuantBR")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Additional configurations can be added here
