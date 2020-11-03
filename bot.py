import slack
import os
from pathlib import Path
from dotenv import load_dotenv

# Importing the .env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Getting the token
token = os.environ['SLACK_TOKEN']

client = slack.WebClient(token=token)

client.chat_postMessage(channel='#bots',text='Hello #bots !')