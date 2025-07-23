from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/forms.body', 'https://www.googleapis.com/auth/forms.responses.readonly']

def create_form(service):
    # Create a new form
    form_body = {
        "info": {
            "title": "Advanced Sample Form Created via API",
        }
    }
    response = service.forms().create(body=form_body).execute()
    print("Form created with ID: ", response.get("formId"))
    return response.get("formId")

def add_question(service, form_id, question_type, question):
    # Add a question to the form
    update = {
        "requests": [{
            "createItem": {
                "item": {
                    "title": question,
                    "questionItem": {
                        "question": {
                            "required": True,
                            "grading": {
                                "pointValue": 1,
                            },
                        }
                    }
                },
                "location": {
                    "index": 0
                }
            }
        }]
    }

    if question_type == "multiple_choice":
        update["requests"][0]["createItem"]["item"]["questionItem"]["question"]["choiceQuestion"] = {
            "type": "RADIO",
            "options": [
                {"value": "Option 1"},
                {"value": "Option 2"},
            ]
        }
    elif question_type == "text":
        update["requests"][0]["createItem"]["item"]["questionItem"]["question"]["textQuestion"] = {}

    service.forms().batchUpdate(formId=form_id, body=update).execute()
    print(f"Added {question_type} question: {question}")

def update_form_settings(service, form_id, title=None, description=None):
    # Update form settings
    update = {}
    if title:
        update["info"] = {"title": title}
    if description:
        update.setdefault("info", {})["description"] = description

    if update:
        service.forms().update(formId=form_id, body=update).execute()
        print(f"Updated form settings: {update}")

def get_responses(service, form_id):
    # Fetch form responses
    responses = []
    page_token = None
    while True:
        response = service.forms().responses().list(formId=form_id, pageToken=page_token).execute()
        responses.extend(response.get("responses", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            break
    return responses

def analyze_responses(responses):
    # Basic analysis of responses
    response_count = len(responses)
    print(f"Total responses: {response_count}")
    # Further analysis can be added based on response structure

def main():
    """Shows advanced usage of the Forms API."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('forms', 'v1', credentials=creds)


if __name__ == '__main__':
    main()