import json
import requests
from typing import Any
from datetime import datetime

# Google Custom Search API settings
API_KEY = "YOUR_API_KEY"
SEARCH_ENGINE_ID = "YOUR_SEARCH_ENGINE_ID"

def google_search(
    search_term: str,
    api_key: str,
    cse_id: str,
    **kwargs: Any,
) -> list[dict[str, str]]:
    params: dict[str, Any] = {
        "q": search_term,
        "key": api_key,
        "cx": cse_id,
        **kwargs,
    }
    response = requests.get(
        "https://www.googleapis.com/customsearch/v1",
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    data: dict[str, Any] = response.json()
    return data.get("items", [])

def extract_info(results: list[dict[str, str]]) -> list[dict[str, str]]:
    info: list[dict[str, str]] = []
    for result in results:
        info.append({
            "title": result["title"],
            "link": result["link"],
            "snippet": result["snippet"],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    return info

def save_to_file(info: list[dict[str, str]], filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=4)

def load_from_file(filename: str) -> list[dict[str, str]]:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data: Any = json.load(f)
            return data if isinstance(data, list) else []
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