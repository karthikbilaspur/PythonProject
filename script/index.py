# pyright: reportMissingTypeStubs=false

import os
from typing import Any, cast

# ============================================================
# PART 1 - GOOGLE FORMS API
# ============================================================
SCOPES = [
    'https://www.googleapis.com/auth/forms.body',
    'https://www.googleapis.com/auth/forms.responses.readonly'
]

def get_forms_service() -> Any | None:
    """Auth and return Forms service. Returns None if setup is missing."""
    try:
        from googleapiclient.discovery import build
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        import pickle
    except ImportError as e:
        print(f"[ERROR] Missing Google libs: {e}")
        print("Run: pip install google-api-python-client google-auth-oauthlib google-auth")
        return None

    creds = None
    if os.path.exists('token.pickle'):
        try:
            with open('token.pickle', 'rb') as f:
                creds = pickle.load(f)
        except Exception:
            print("[WARN] token.pickle corrupt - re-authenticating.")
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None
        if not creds:
            if not os.path.exists('credentials.json'):
                print("[ERROR] credentials.json not found. Download it from Google Cloud Console > APIs > Credentials > OAuth client ID (Desktop).")
                return None
            flow = cast(Any, InstalledAppFlow).from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as f:
            pickle.dump(creds, f)

    return cast(Any, build('forms', 'v1', credentials=creds))

def create_form(service: Any, title: str, description: str = "") -> str:
    body = {"info": {"title": title, "documentTitle": title}}
    if description:
        body["info"]["description"] = description
    result = service.forms().create(body=body).execute()
    form_id = result["formId"]
    print(f"[CREATED] {title} | ID: {form_id}")
    print(f"URL: https://docs.google.com/forms/d/{form_id}/edit")
    return form_id

def add_questions_batch(service: Any, form_id: str, questions: list[dict[str, Any]]) -> None:
    """questions: list of dicts, see main() for examples. Supports text, paragraph,
    multiple_choice, checkbox, dropdown, scale, date."""
    requests: list[dict[str, Any]] = []
    for index, q in enumerate(questions):
        q_type = q.get("type")
        item: dict[str, Any] = {"title": q["title"], "questionItem": {"question": {"required": q.get("required", True)}}}
        qq = cast(dict[str, Any], item["questionItem"]["question"])
        opts = q.get("options", [])
        if q_type == "text":
            qq["textQuestion"] = {}
        elif q_type == "paragraph":
            qq["textQuestion"] = {"paragraph": True}
        elif q_type in ("multiple_choice", "checkbox", "dropdown"):
            type_map = {"multiple_choice": "RADIO", "checkbox": "CHECKBOX", "dropdown": "DROP_DOWN"}
            qq["choiceQuestion"] = {
                "type": type_map[q_type],
                "options": [{"value": o} for o in (opts or ["Option 1", "Option 2"])],
                "shuffle": q.get("shuffle", False),
            }
        elif q_type == "scale":
            qq["scaleQuestion"] = {
                "low": q.get("low", 1), "high": q.get("high", 5),
                "lowLabel": q.get("low_label", ""), "highLabel": q.get("high_label", ""),
            }
        elif q_type == "date":
            qq["dateQuestion"] = {}
        else:
            raise ValueError(f"Unknown question type: {q_type!r}. Use text/paragraph/multiple_choice/checkbox/dropdown/scale/date")
        requests.append({"createItem": {"item": item, "location": {"index": index}}})
    service.forms().batchUpdate(formId=form_id, body={"requests": requests}).execute()
    print(f"[ADDED] {len(questions)} questions")

def update_form_info(service: Any, form_id: str, title: str | None = None, description: str | None = None) -> None:
    info: dict[str, str] = {}
    if title:
        info["title"] = title; info["documentTitle"] = title
    if description:
        info["description"] = description
    if not info:
        print("Nothing to update.")
        return
    service.forms().batchUpdate(formId=form_id, body={"requests": [{
        "updateFormInfo": {"info": info, "updateMask": ",".join(info.keys())}
    }]}).execute()
    print(f"[UPDATED] {info}")

def get_responses(service: Any, form_id: str, limit: int = 5) -> list[dict[str, Any]]:
    responses: list[dict[str, Any]] = []
    page_token = None
    while True:
        resp = service.forms().responses().list(formId=form_id, pageToken=page_token).execute()
        responses.extend(resp.get("responses", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    print(f"[INFO] Total responses: {len(responses)}")
    for r in responses[:limit]:
        print(f"--- {r.get('responseId')} @ {r.get('createTime')} ---")
        answer_map = cast(dict[str, Any], r.get("answers") or {})
        for qid, raw_answer in answer_map.items():
            answer = cast(dict[str, Any], raw_answer)
            text_answers = cast(dict[str, Any], answer.get("textAnswers") or {})
            text_answer_items = cast(list[dict[str, Any]], text_answers.get("answers") or [])
            vals = [cast(str, item.get("value", "")) for item in text_answer_items]
            print(f"  {qid}: {', '.join(vals) if vals else answer}")
    return responses

def run_forms_demo():
    service = get_forms_service()
    if not service:
        return
    form_id = create_form(service, "Advanced Sample Form Created via API",
                          "This form was auto-generated by Python")
    questions: list[dict[str, Any]] = [
        {"type": "text", "title": "What is your full name?"},
        {"type": "text", "title": "What is your email?"},
        {"type": "multiple_choice", "title": "How did you hear about us?", "options": ["Google", "Friend", "LinkedIn", "Other"]},
        {"type": "checkbox", "title": "What are you interested in?", "options": ["Python", "AI/ML", "Web Dev", "Cloud"]},
        {"type": "scale", "title": "How likely are you to recommend us?", "low": 1, "high": 5, "low_label": "Not at all", "high_label": "Very likely"},
        {"type": "paragraph", "title": "Any additional feedback?", "required": False},
    ]
    add_questions_batch(service, form_id, questions)
    # get_responses(service, form_id)  # will be 0 for a new form

# ============================================================
# PART 2 - UBUNTU SCRAPER
# ============================================================
HEADERS = {"User-Agent": "Mozilla/5.0 (personal learning project; contact: you@example.com)"}
NEWS_URL = "https://ubuntu.com/blog"
DOWNLOADS_URL = "https://ubuntu.com/download"

def _soup(url: str):
    import requests
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None, urljoin
    return BeautifulSoup(r.text, 'html.parser'), urljoin

def scrape_ubuntu_news(url: str):
    soup, join = _soup(url)
    if soup is None:
        return
    articles = soup.find_all('article')
    if not articles:
        print("No <article> tags found - ubuntu.com/blog layout may have changed.")
        return
    for a in articles:
        title = a.find('h2') or a.find('h3')
        link = a.find('a', href=True)
        if title and link:
            href = link.get('href')
            if not isinstance(href, str):
                continue
            print(f"Title: {title.get_text(strip=True)}")
            print(f"Link: {join(url, href)}")
            print()

def scrape_ubuntu_downloads(url: str):
    soup, join = _soup(url)
    if soup is None:
        return
    seen: set[str] = set()
    # Primary: old class. Fallback: any link to .iso or /download/
    candidates = soup.find_all('a', class_='download-link')
    if not candidates:
        candidates = [a for a in soup.find_all('a', href=True)
                      if '.iso' in a['href'] or '/download' in a['href']]
    if not candidates:
        print("No download links found - page layout may have changed.")
        return
    for link in candidates:
        href_value = link.get('href')
        if not isinstance(href_value, str):
            continue
        href = join(url, href_value)
        if href not in seen:
            seen.add(href)
            print(f"Download Link: {href}  |  Text: {link.get_text(strip=True)[:60]}")

def run_scraper_menu():
    while True:
        print("\nUbuntu Scraper Menu:")
        print("1. Scrape News")
        print("2. Scrape Downloads")
        print("3. Back")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            scrape_ubuntu_news(NEWS_URL)
        elif choice == "2":
            scrape_ubuntu_downloads(DOWNLOADS_URL)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

# ============================================================
# MAIN MENU
# ============================================================
def main():
    while True:
        print("\n=== Merged Suite ===")
        print("1. Google Forms - create sample form via API")
        print("2. Google Forms - fetch responses for an existing form")
        print("3. Ubuntu Scraper")
        print("0. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            run_forms_demo()
        elif choice == "2":
            service = get_forms_service()
            if service:
                fid = input("Enter form ID: ").strip()
                if fid:
                    get_responses(service, fid)
        elif choice == "3":
            run_scraper_menu()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
