
import argparse
import json
import os
import re
import time
from datetime import datetime
from typing import Any

import requests

try:
    from requests_oauthlib import OAuth2Session
except ImportError:
    OAuth2Session = None  # type: ignore

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None  # type: ignore

try:
    import pandas as pd
except ImportError:
    pd = None  # type: ignore


# ---------- helpers ----------
def safe_filename(name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*]', "_", name).strip() or "search"
    return name[:80]

def _text(el: Any) -> str:
    return el.get_text(strip=True) if el is not None else ""


# ---------- 1. Google Custom Search ----------
def google_search(search_term: str, api_key: str, cse_id: str, **kwargs: Any) -> list[dict[str, Any]]:
    params: dict[str, Any] = {"q": search_term, "key": api_key, "cx": cse_id, **kwargs}
    resp = requests.get("https://www.googleapis.com/customsearch/v1", params=params, timeout=30)
    resp.raise_for_status()
    return resp.json().get("items", []) or []

def extract_info(results: list[dict[str, Any]]) -> list[dict[str, str]]:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return [{
        "title": str(r.get("title", "")),
        "link": str(r.get("link", "")),
        "snippet": str(r.get("snippet", "")),
        "date": now,
    } for r in results]

def save_to_file(info: list[dict[str, str]], filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=4, ensure_ascii=False)

def load_from_file(filename: str) -> list[dict[str, Any]]:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                return []
            return [item for item in data if isinstance(item, dict)]
    except FileNotFoundError:
        return []

def run_google_search() -> None:
    api_key = os.getenv("GOOGLE_API_KEY", "YOUR_API_KEY")
    cse_id = os.getenv("GOOGLE_CSE_ID", "YOUR_SEARCH_ENGINE_ID")
    if api_key in ("", "YOUR_API_KEY"):
        print("Set GOOGLE_API_KEY env var first.")
        return
    term = input("Enter your search term: ").strip()
    if not term:
        print("Empty search term.")
        return
    results = google_search(term, api_key, cse_id, num=10)
    info = extract_info(results)
    filename = f"{safe_filename(term)}.json"
    save_to_file(info, filename)
    print(f"Results saved to {filename} ({len(info)} items)")
    for item in load_from_file(filename):
        print(f"Title: {item.get('title')}\nLink: {item.get('link')}\nSnippet: {item.get('snippet')}\nDate: {item.get('date')}\n")


# ---------- 2. LinkedIn (legacy) ----------
LINKEDIN_AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
LINKEDIN_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
LINKEDIN_SCOPE = ["w_share", "r_liteprofile"]  # LEGACY - see header

def linkedin_config() -> tuple[str, str, str]:
    return (
        os.getenv("LINKEDIN_CLIENT_ID", "YOUR_CLIENT_ID"),
        os.getenv("LINKEDIN_CLIENT_SECRET", "YOUR_CLIENT_SECRET"),
        os.getenv("LINKEDIN_REDIRECT_URI", "YOUR_REDIRECT_URI"),
    )

def get_access_token() -> str | None:
    if OAuth2Session is None:
        print("Install requests_oauthlib: pip install requests_oauthlib")
        return None
    client_id, client_secret, redirect_uri = linkedin_config()
    if os.path.exists("token.json"):
        with open("token.json", "r", encoding="utf-8") as f:
            token: dict[str, Any] = json.load(f)
        return token.get("access_token")
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=LINKEDIN_SCOPE)
    auth_url: str = oauth.authorization_url(LINKEDIN_AUTH_URL)[0]  # type: ignore[reportUnknownMemberType]
    print(f"Please go to {auth_url} and authorize the app.")
    auth_response = input("Enter the full callback URL: ").strip()
    token = oauth.fetch_token(  # type: ignore[reportUnknownMemberType]
        LINKEDIN_TOKEN_URL,
        client_secret=client_secret,
        authorization_response=auth_response,
    )
    with open("token.json", "w", encoding="utf-8") as f:
        json.dump(token, f)
    return token.get("access_token")

def refresh_access_token(refresh_token: str) -> str | None:
    # FIXED: missing closing brace in original typed version
    client_id, client_secret, _ = linkedin_config()
    data: dict[str, str] = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
    }
    resp = requests.post(LINKEDIN_TOKEN_URL, headers={"Content-Type": "application/x-www-form-urlencoded"}, data=data, timeout=30)
    resp.raise_for_status()
    return resp.json().get("access_token")

def post_update(access_token: str, text: str, media: dict[str, str] | None = None) -> None:
    url = "https://api.linkedin.com/v2/shares"  # LEGACY endpoint
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json", "X-Restli-Protocol-Version": "2.0.0"}
    post: dict[str, Any] = {"shareMediaCategory": "NONE", "text": {"text": text}}
    data: dict[str, Any] = {
        "lifecycleState": "PUBLISHED",
        "specificContent": {"com.linkedin.ugc.Post": post},
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }
    if media:
        post["shareMediaCategory"] = "ARTICLE"
        post["media"] = [{
            "status": "READY",
            "description": {"text": media.get("description", "")},
            "originalUrl": media.get("url", ""),
            "title": {"text": media.get("title", "")},
        }]
    resp = requests.post(url, headers=headers, json=data, timeout=30)
    if resp.status_code == 201:
        print("Update posted successfully!")
    else:
        print(f"Error posting update ({resp.status_code}): {resp.text}")

def get_profile(access_token: str) -> dict[str, Any]:
    resp = requests.get("https://api.linkedin.com/v2/me", headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}, timeout=30)
    resp.raise_for_status()
    return resp.json()

def run_linkedin() -> None:
    token = get_access_token()
    if not token:
        print("Unable to obtain an access token.")
        return
    while True:
        print("\n1. Post update\n2. Get profile\n3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            text = input("Enter your LinkedIn update text: ")
            media: dict[str, str] | None = None
            if input("Do you want to add media? (yes/no): ").lower() == "yes":
                media = {"title": input("Enter media title: "), "description": input("Enter media description: "), "url": input("Enter media URL: ")}
            post_update(token, text, media)
        elif choice == "2":
            try:
                print(json.dumps(get_profile(token), indent=4))
            except Exception as e:
                print(f"Error getting profile: {e}")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")


# ---------- 3. Job Scraper (best-effort, may return 0 due to blocking) ----------
class JobScraper:
    def __init__(self, job_title: str, location: str):
        self.job_title = job_title
        self.location = location
        self.job_listings: list[dict[str, str]] = []

    def _get_soup(self, url: str):
        if BeautifulSoup is None:
            print("Install beautifulsoup4: pip install beautifulsoup4")
            return None
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        resp.raise_for_status()
        return BeautifulSoup(resp.content, "html.parser")

    def scrape_indeed_jobs(self) -> None:
        soup = self._get_soup(f"https://www.indeed.com/jobs?q={self.job_title}&l={self.location}")
        if soup is None:
            return
        # Legacy selector + fallback to newer Indeed markup
        cards = soup.find_all("div", class_="jobsearch-SerpJobCard") or soup.select("div.job_seen_beacon")
        for job in cards:
            self.job_listings.append({
                "Title": _text(job.find("h2", class_="title") or job.select_one("h2.jobTitle")),
                "Company": _text(job.find("span", class_="company") or job.select_one('[data-testid="company-name"]')),
                "Location": _text(job.find("div", class_="location") or job.select_one('[data-testid="text-location"]')),
                "Description": _text(job.find("div", class_="summary")),
                "Source": "Indeed",
            })

    def scrape_linkedin_jobs(self) -> None:
        soup = self._get_soup(f"https://www.linkedin.com/jobs/search/?keywords={self.job_title}&location={self.location}")
        if soup is None:
            return
        for job in soup.find_all("li", class_="jobs-search-results__list-item") or soup.select("li.jobs-search-results__list-item"):
            self.job_listings.append({
                "Title": _text(job.find("h3", class_="base-search-card__title")),
                "Company": _text(job.find("h4", class_="base-search-card__subtitle")),
                "Location": _text(job.find("span", class_="job-search-card__location")),
                "Description": _text(job.find("span", class_="job-card-container__snippet")),
                "Source": "LinkedIn",
            })

    def scrape_glassdoor_jobs(self) -> None:
        soup = self._get_soup(f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={self.job_title}&locT=C&locId=&locKeyword={self.location}")
        if soup is None:
            return
        for job in soup.find_all("li", class_="jl"):
            self.job_listings.append({
                "Title": _text(job.find("div", class_="title")),
                "Company": _text(job.find("div", class_="company")),
                "Location": _text(job.find("span", class_="subtle loc")),
                "Description": _text(job.find("span", class_="job-description")),
                "Source": "Glassdoor",
            })

    def save_to_csv(self) -> str:
        if pd is None:
            print("Install pandas: pip install pandas")
            return ""
        filename = f"{safe_filename(self.job_title)}_{safe_filename(self.location)}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        pd.DataFrame(self.job_listings).to_csv(filename, index=False)
        return filename

def run_job_scraper_cli(args: argparse.Namespace) -> None:
    scraper = JobScraper(args.job_title, args.location)
    for site in args.sites:
        try:
            getattr(scraper, f"scrape_{site}_jobs")()
        except Exception as e:
            print(f"{site}: failed ({e}) - site likely blocked / changed HTML")
        time.sleep(1)
    filename = scraper.save_to_csv()
    print(f"Job listings scraped: {len(scraper.job_listings)} jobs found" + (f" -> {filename}" if filename else ""))


# ---------- main ----------
def main() -> None:
    parser = argparse.ArgumentParser(description="Consolidated Toolkit")
    parser.add_argument("--job", action="store_true", help="Run job scraper non-interactively")
    parser.add_argument("-j", "--job_title", help="Job title to search for")
    parser.add_argument("-l", "--location", help="Location to search in")
    parser.add_argument("-s", "--sites", nargs="+", choices=["indeed", "linkedin", "glassdoor"], help="Job boards to scrape")
    args = parser.parse_args()
    if args.job:
        if not args.job_title or not args.location or not args.sites:
            parser.error("--job requires -j/--job_title, -l/--location, -s/--sites")
        run_job_scraper_cli(args)
        return
    while True:
        print("\n=== Consolidated Toolkit ===")
        print("1. Google Search -> JSON")
        print("2. LinkedIn Poster / Profile (legacy API)")
        print("3. Job Scraper (interactive)")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            run_google_search()
        elif choice == "2":
            run_linkedin()
        elif choice == "3":
            if BeautifulSoup is None:
                print("Install: pip install beautifulsoup4 pandas")
                continue
            jt = input("Job title: ").strip()
            loc = input("Location: ").strip()
            sites = input("Sites (space separated, indeed linkedin glassdoor): ").strip().split()
            ns = argparse.Namespace(job_title=jt, location=loc, sites=[s for s in sites if s in ("indeed", "linkedin", "glassdoor")])
            run_job_scraper_cli(ns)
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
