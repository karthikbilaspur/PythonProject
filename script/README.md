# Script

Features
1.Google Forms (via API)

Create a form with title + description
Add questions in one batch (much faster than one-by-one)
Question types: text, paragraph, multiple_choice, checkbox, dropdown, scale, date
Update a form's title / description
Fetch responses with pagination + readable summary (not raw dicts)
Auto re-auth if token.pickle is corrupt or expired

Requirements
Python 3.10+
A Google account (only for the Forms part — the scraper works without it)
pip install google-api-python-client google-auth-oauthlib google-auth requests beautifulsoup4
Setup — Google Forms part (one-time, ~5 min)
Go to Google Cloud Console

Create a project (or use an existing one)
APIs & Services → Library → enable Google Forms API
APIs & Services → Credentials → Create Credentials → OAuth client ID
Application type: Desktop app
Download the JSON → rename it to credentials.json → put it next to merged_forms_scraper.py
First run: a browser window opens, sign in with Google, click Allow
token.pickle is saved — you won't have to sign in again unless it expires
⚠️ Never commit credentials.json or token.pickle to GitHub. They are your login keys. Add them to .gitignore (see below).

Usage
python merged_forms_scraper.py
=== Merged Suite ===
1.Google Forms - create sample form via API
2. Google Forms - fetch responses for an existing form
3. Ubuntu Scraper
0. Exit

Option 1 — Create a sample form
Creates a form called "Advanced Sample Form Created via API" with:

Full name (text), Email (text)
How did you hear about us? (multiple choice)
What are you interested in? (checkbox)
How likely are you to recommend us? (scale 1–5)
Any additional feedback? (paragraph, optional)
It prints the form ID and edit URL, e.g.:

[CREATED] Advanced Sample Form Created via API | ID: 1FAIpQLS...
URL: [https://docs.google.com/forms/d/1FAIpQLS.../edit](https://docs.google.com/forms/d/1FAIpQLS.../edit)

2.Back
Using it as a library (not just the menu)
from merged_forms_scraper import (
    get_forms_service, create_form,
    add_questions_batch, get_responses,
    scrape_ubuntu_news, scrape_ubuntu_downloads,
)

service = get_forms_service()
form_id = create_form(service, "My Survey", "Please fill this in")

add_questions_batch(service, form_id, [
    {"type": "text", "title": "What is your name?"},
    {"type": "multiple_choice", "title": "Favourite language?",
     "options": ["Python", "JS", "Go"], "shuffle": True},
    {"type": "scale", "title": "Rate this 1-5",
     "low": 1, "high": 5, "low_label": "Bad", "high_label": "Great"},
    {"type": "date", "title": "When are you free?"},
    {"type": "paragraph", "title": "Comments?", "required": False},
])

responses = get_responses(service, form_id)

scrape_ubuntu_news("https://ubuntu.com/blog")
scrape_ubuntu_downloads("https://ubuntu.com/download")

## Question dict format

| Key | Required | Notes |
| --- | --- | --- |
| type | Yes | text / paragraph / multiple_choice / checkbox / dropdown / scale / date |
| title | Yes | The question text |
| options | For choice types | List of strings, e.g. `["Python", "JS"]` |
| required | No | Default True |
| shuffle | No | Choice questions only, default False |
| low / high | No | Scale only, default 1 / 5 |
| low_label / high_label | No | Scale only |

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `credentials.json` not found | Download the OAuth Desktop client JSON from Cloud Console and rename it to `credentials.json` |
| `token.pickle` corrupt | Delete `token.pickle` and run again — it re-auths |
| No article tags found / No download links found | ubuntu.com changed its layout. The scraper has a fallback, but check the site manually |
| googletrans / import errors | Not needed for this project — only the packages in Requirements |
| Browser doesn't open on first login | Copy the URL printed in the terminal into your browser manually |
 gitignore (recommended) credentials.json token.pickle.

__pycache__/
*.pyc
Notes / Limits
The Forms API can create questions and read responses, but it cannot change a form's theme, or read responses that need extra permissions.
The scraper is for light personal use. ubuntu.com changes layout often — if it prints "layout may have changed", that's the site, not your code.
This is a learning / utility project, not production code. Don't put real secrets in a form, and don't scrape aggressively.
License
MIT — do what you want with it, just don't share your credentials.json / token.pickle.
