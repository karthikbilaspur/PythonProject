import os
import json
import requests
from googleapiclient.discovery import build
from datetime import datetime

# Google Custom Search API settings
API_KEY = "YOUR_API_KEY"
SEARCH_ENGINE_ID = "YOUR_SEARCH_ENGINE_ID"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res["items"]

def extract_info(results):
    info = []
    for result in results:
        info.append({
            "title": result["title"],
            "link": result["link"],
            "snippet": result["snippet"],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    return info

def save_to_file(info, filename):
    with open(filename, "w") as f:
        json.dump(info, f, indent=4)

def load_from_file(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def main():
    search_term = input("Enter your search term: ")
    results = google_search(search_term, API_KEY, SEARCH_ENGINE_ID, num=10)
    info = extract_info(results)
    filename = f"{search_term}.json"
    save_to_file(info, filename)
    print(f"Results saved to {filename}")
    loaded_info = load_from_file(filename)
    for item in loaded_info:
        print(f"Title: {item['title']}")
        print(f"Link: {item['link']}")
        print(f"Snippet: {item['snippet']}")
        print(f"Date: {item['date']}\n")

if __name__ == "__main__":
    main()