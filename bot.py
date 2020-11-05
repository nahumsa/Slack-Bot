import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, Request, Response
from slackeventsapi import SlackEventAdapter

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

def parse_text_greeting(text, word='Hello'):
    """ Parse recieved text to return a greeting.

    Args:
        text (string): string recieved from slack POST.
        word (str, optional): Word that you want in your text. Defaults to 'Hello'.

    Returns:
        string: Returns a string with a greeting or another if the greeting
        is not in the text

    """
    special_characters = [' ', '!', '.', ',']
    for char in special_characters:
        if word in text.split(char):
            return "Hi, Human!"
    return "I can't Understand you."

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    
    if user_id != BOT_ID:
        return_text = parse_text_greeting(text)
        client.chat_postMessage(channel=channel_id,text=return_text)

@app.route('/message-count')
def message_count():
    return Response(), 200

if __name__ == '__main__':
    app.run(debug=True)