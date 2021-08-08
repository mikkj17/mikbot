import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('LIVESCORE_API_KEY')
API_SECRET = os.getenv('LIVESCORE_API_SECRET')
BASE_API_URL = 'https://livescore-api.com/api-client'
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
MONGO_CONNECTION_URL = os.getenv('MONGO_CONNECTION_URL')