# Google Forms API Project
=====================================

This project demonstrates advanced usage of the Google Forms API using Python. It covers creating a form, adding questions, updating form settings, fetching responses, and performing basic analysis on the responses.

## Prerequisites
---------------

*   Google Cloud Platform project with the Google Forms API enabled
*   OAuth 2.0 credentials set up (OAuth client ID for a desktop application)
*   `google-api-python-client`, `google-auth-httplib2`, and `google-auth-oauthlib` libraries installed
*   Python 3.6 or later

## Setup
--------

1.  Create a new Google Cloud Platform project and enable the Google Forms API.
2.  Set up OAuth 2.0 credentials by creating a new OAuth client ID for a desktop application. Download the `credentials.json` file.
3.  Install the required libraries using pip:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
Clone this repository or download the code.
Usage
Run the main.py script to create a new form, add questions, update form settings, fetch responses, and perform basic analysis:
Bash