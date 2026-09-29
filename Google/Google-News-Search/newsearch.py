import requests
import json
from datetime import datetime

# Google Custom Search JSON API settings
API_KEY = "YOUR_API_KEY"
SEARCH_ENGINE_ID = "YOUR_SEARCH_ENGINE_ID"
QUERY = "latest news"

def get_news():
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={QUERY}"
    response = requests.get(url)
    data = json.loads(response.text)
    news = []
    for item in data["items"]:
        news.append({
            "title": item["title"],
            "link": item["link"],
            "snippet": item["snippet"]
        })
    return news

def send_newsletter(news):
    # Replace with your email sending logic
    print("Sending newsletter...")
    for item in news:
        print(f"Title: {item['title']}")
        print(f"Link: {item['link']}")
        print(f"Snippet: {item['snippet']}")
        print("")

def main():
    news = get_news()
    send_newsletter(news)

if __name__ == "__main__":
    main()