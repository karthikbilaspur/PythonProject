import os
import json
import requests
from flask import Flask, request
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import logging

app = Flask(__name__)

# Facebook App settings
PAGE_ACCESS_TOKEN = "YOUR_PAGE_ACCESS_TOKEN"
VERIFY_TOKEN = "YOUR_VERIFY_TOKEN"

# Facebook Messenger API endpoint
FB_API_URL = "https://graph.facebook.com/v13.0/me/messages"

# NLP settings
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def send_message(recipient_id, message):
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message
        }
    })
    response = requests.post(FB_API_URL, params=params, headers=headers, data=data)
    if response.status_code != 200:
        logging.error(f"Error sending message: {response.text}")

def handle_message(message):
    recipient_id = message["sender"]["id"]
    message_text = message["message"]["text"]
    tokens = word_tokenize(message_text)
    tokens = [token.lower() for token in tokens if token.isalpha()]
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    response_message = process_message(tokens)
    send_message(recipient_id, response_message)

def process_message(tokens):
    # Implement your NLP logic here
    if "hello" in tokens:
        return "Hello! How can I assist you today?"
    elif "help" in tokens:
        return "I can help you with various tasks. What do you need help with?"
    else:
        return "I didn't understand that. Can you please rephrase?"

@app.route("/", methods=["GET"])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge"), 200
        else:
            return "Invalid verify token", 403
    else:
        return "Hello, world!", 200

@app.route("/", methods=["POST"])
def handle_incoming_messages():
    data = request.get_json()
    if data["object"] == "page":
        for entry in data["entry"]:
            for message in entry["messaging"]:
                if message.get("message"):
                    handle_message(message)
    return "ok", 200

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)