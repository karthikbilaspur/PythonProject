# Google Meet

link for a meeting with the specified summary, description, start time, end time, and attendees. You'll need to replace the credentials.json file with your own credentials file and install the required libraries.
How it works:
The script uses the Google Calendar API to create an event with a Google Meet link.
The create_event function takes in the service object, summary, description, start time, end time, and attendees as parameters.
The function creates an event body with the specified details and conference data.
The service.events().insert() method is used to create the event and get the Meet link.
The Meet link is then printed to the console.
Note: This script assumes you have the google-api-python-client and google-auth-httplib2 libraries installed. You'll need to install these libraries using pip:
Bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
