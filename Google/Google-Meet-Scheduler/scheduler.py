import datetime
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def create_event(service, summary, description, start_time, end_time, attendees):
    event = {
        'summary': summary,
        'description': description,
        'start': {'dateTime': start_time, 'timeZone': 'America/New_York'},
        'end': {'dateTime': end_time, 'timeZone': 'America/New_York'},
        'attendees': [{'email': attendee} for attendee in attendees],
        'conferenceData': {
            'createRequest': {
                'requestId': 'some-random-id',
                'conferenceSolutionKey': {'type': 'hangoutsMeet'}
            }
        }
    }
    event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
    return event.get('hangoutLink')

def main():
    """Shows basic usage of the Google Calendar API.
    Lists the next 10 events on the user's calendar.
    """
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

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    summary = 'Test Meeting'
    description = 'This is a test meeting'
    start_time = (datetime.datetime.now() + datetime.timedelta(minutes=10)).isoformat()
    end_time = (datetime.datetime.now() + datetime.timedelta(minutes=30)).isoformat()
    attendees = ['attendee1@example.com', 'attendee2@example.com']
    meet_link = create_event(service, summary, description, start_time, end_time, attendees)
    print('Meet link:', meet_link)

if __name__ == '__main__':
    main()