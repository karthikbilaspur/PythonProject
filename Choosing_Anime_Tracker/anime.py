import requests
from bs4 import BeautifulSoup
import json

def get_upcoming_anime(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.find_all('h2')

    upcoming_anime = [title.text.strip() for title in titles]
    return upcoming_anime

def get_anime_info(title):
    url = f"https://api.jikan.moe/v4/anime?q={title}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

    data = json.loads(response.text)
    if data['data']:
        anime_info = {
            'title': data['data'][0]['title'],
            'rating': data['data'][0].get('score', 'Unknown'),
            'synopsis': data['data'][0].get('synopsis', 'Unknown'),
            'creators': data['data'][0].get('producers', [])
        }
        return anime_info
    else:
        return None

def main():
    url = "https://www.crunchyroll.com/news"
    upcoming_anime = get_upcoming_anime(url)
    for anime in upcoming_anime:
        anime_info = get_anime_info(anime)
        if anime_info:
            print(f"**Title:** {anime_info['title']}")
            print(f"**Rating:** {anime_info['rating']}")
            print(f"**Synopsis:** {anime_info['synopsis']}")
            print(f"**Creators:** {[creator['name'] for creator in anime_info['creators']]}")
            print("\n")

if __name__ == "__main__":
    main()