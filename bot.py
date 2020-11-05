import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from slackeventsapi import SlackEventAdapter

from flask import Flask, request, Response

from helpers import parse_text_greeting

# Importing the .env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Getting environmental varibles
token = os.environ['SLACK_TOKEN']
signing_secret = os.environ['SIGNING_SECRET']

# Loading flask app
app = Flask(__name__)

# Set up Slack Events
slack_event_adapter = SlackEventAdapter(signing_secret, '/slack/events',app)

# Set up slack client
client = slack.WebClient(token=token)
BOT_ID = client.api_call("auth.test")['user_id']

# PUT THIS ON A DATABASE
message_counts = {}

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    
    if user_id != BOT_ID:
        
        if user_id in message_counts:
            message_counts[user_id] += 1
        else:
            message_counts[user_id] = 1

        return_text = parse_text_greeting(text)
        client.chat_postMessage(channel=channel_id,text=return_text)

@app.route('/message-count', methods=['POST','GET'])
def message_count():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    n_messages = message_counts.get(user_id, 0)
    
    # Check if you are testing the app
    if not app.testing:
        client.chat_postMessage(channel=channel_id,text=f"Message: {n_messages}")
    
    return Response(), 200

if __name__ == '__main__':
    app.run(debug=True)