
import json
from typing import Any

from flask import Flask, Response, request
import requests

# Token that has to be generated from webhook page portal
ACCESS_TOKEN = "random token"
# Token that has to be added for verification with developer portal
VERIFICATION_TOKEN = "abc"
# Identifier payloads for initial button
BC_INDIA = "BC_INDIA"
BC_SYMPTOMS = "BC_SYMPTOMS"
BC_RISK_FACTORS = "BC_RISK_FACTORS"

app = Flask(__name__)

# This get endpoint is for verification with messenger app
@app.route('/webhook', methods=['GET'])  # type: ignore[reportUntypedFunctionDecorator]
def webhook() -> Response:
    verify_token = request.args.get("hub.verify_token")
    if verify_token == VERIFICATION_TOKEN:
        challenge = request.args.get("hub.challenge")
        return Response(challenge or "", mimetype="text/plain")
    return Response("Unable to authorise.", status=403, mimetype="text/plain")

@app.route("/webhook", methods=['POST'])  # type: ignore[reportUntypedFunctionDecorator]
def webhook_handle() -> Response:
    data: dict[str, Any] = request.get_json(silent=True) or {}

    if data["object"] == "page":  
        for entry in data["entry"]:
            for event in entry["messaging"]:
                if event.get("message"):  
                    process_message(event)
                elif event.get("postback"):
                    process_postback(event)
    return Response("ok", mimetype="text/plain")

def process_message(event: dict[str, Any]) -> None:
    sender_id = event["sender"]["id"]
    if "text" in event["message"]:
        send_initial_menu(sender_id)

def send_initial_menu(sender_id: str):
    message_data = json.dumps({
        "recipient": {
            "id": sender_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [{
                        "title": "Breast Cancer India Stats",
                        "subtitle": "Get the breast cancer statistics in India",
                        "buttons": [{
                            "type": "postback",
                            "title": "Get Breast Cancer Statistics",
                            "payload": BC_INDIA,
                        }, {
                            "type": "postback",
                            "title": "Breast Cancer Symptoms",
                            "payload": BC_SYMPTOMS,
                        }, {
                            "type": "postback",
                            "title": "Breast Cancer Risk Factors",
                            "payload": BC_RISK_FACTORS,
                        }],
                    }]
                }
            }
        }
    })
    call_send_api(message_data)

def send_breast_cancer_stats(sender_id: str):
    # Hardcoded statistics for demonstration purposes
    new_cases = 162468
    mortality = 87090
    message_data = json.dumps({
        "recipient": {
            "id": sender_id
        },
        "message": {
            "text": f"Breast Cancer Statistics in India:\nNew Cases: {new_cases}\nMortality: {mortality}"
        }
    })
    call_send_api(message_data)

def send_breast_cancer_symptoms(sender_id: str):
    symptoms = "Common symptoms of breast cancer include:\n* A lump or thickening in the breast or underarm area\n* Change in the size or shape of the breast\n* Dimpling or puckering of the skin\n* Redness or scaliness of the skin"
    message_data = json.dumps({
        "recipient": {
            "id": sender_id
        },
        "message": {
            "text": symptoms
        }
    })
    call_send_api(message_data)

def send_breast_cancer_risk_factors(sender_id: str):
    risk_factors = "Risk factors for breast cancer include:\n* Family history of breast cancer\n* Age (risk increases with age)\n* Genetic mutations (e.g. BRCA1, BRCA2)"
    message_data = json.dumps({
        "recipient": {
            "id": sender_id
        },
        "message": {
            "text": risk_factors
        }
    })
    call_send_api(message_data)

def process_postback(event: dict[str, Any]) -> None:
    sender_id = event["sender"]["id"]
    payload = event["postback"]["payload"]
    if payload == BC_INDIA:
        send_breast_cancer_stats(sender_id)
    elif payload == BC_SYMPTOMS:
        send_breast_cancer_symptoms(sender_id)
    elif payload == BC_RISK_FACTORS:
        send_breast_cancer_risk_factors(sender_id)

def call_send_api(message_data: str) -> None:
    params = {
        "access_token":  ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    requests.post("https://graph.facebook.com/v5.0/me/messages",
                  params=params, headers=headers, data=message_data)

if __name__ == "__main__":
    app.run()