import json
from typing import Any

import requests
from flask import Flask, Response, request
from nltk.tokenize import word_tokenize  # type: ignore[import-untyped]
from nltk.corpus import stopwords  # type: ignore[import-untyped]p
from nltk.stem import WordNetLemmatizer  # type: ignore[import-untyped]
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

def send_message(recipient_id: str, message: str) -> None:
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

def handle_message(message: dict[str, Any]) -> None:
    recipient_id = message["sender"]["id"]
    message_text = message["message"]["text"]
    tokens: list[str] = word_tokenize(message_text)
    tokens = [token.lower() for token in tokens if token.isalpha()]
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    response_message = process_message(tokens)
    send_message(recipient_id, response_message)

def process_message(tokens: list[str]) -> str:
    # Implement your NLP logic here
    if "hello" in tokens:
        return "Hello! How can I assist you today?"
    elif "help" in tokens:
        return "I can help you with various tasks. What do you need help with?"
    else:
        return "I didn't understand that. Can you please rephrase?"

@app.route("/", methods=["GET"])
def verify() -> Response:
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return Response(request.args.get("hub.challenge"), status=200)
        else:
            return Response("Invalid verify token", status=403)
    else:
        return Response("Hello, world!", status=200)

@app.route("/", methods=["POST"])
def handle_incoming_messages() -> Response:
    data: dict[str, Any] = request.get_json()
    if data["object"] == "page":
        for entry in data["entry"]:
            for message in entry["messaging"]:
                if message.get("message"):
                    handle_message(message)
    return Response("ok", status=200)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)