from os.path import join, dirname
from dotenv import load_dotenv
import os

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Gets secure API and DB information from the .env file and stores it in our assigned variable. 
SLACK_CLIENT_TOKEN = os.getenv("SLACK_CLIENT_TOKEN")
