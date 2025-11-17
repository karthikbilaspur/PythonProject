import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_toi_news():
    """
    Scrapes news headlines and links from Times of India website.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'
    }

    try:
        # Access TOI webpage disguised as a browser
        response = requests.get('https://timesofindia.indiatimes.com/', headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

    soup = BeautifulSoup(response.text, 'lxml')
    news_headlines = []
    news_links = []

    for article in soup.find_all('div', class_='col_l_6'):
        figcaption = article.find('figcaption')
        if figcaption is not None:
            # Extract news headline and link
            link = article.find('a').get("href")
            headline = figcaption.text.strip()

            news_headlines.append(headline)
            news_links.append(link)

    # Create a Pandas DataFrame
    df = pd.DataFrame({'News Headline': news_headlines, 'News Link': news_links})
    return df

if __name__ == "__main__":
    toi_headlines = scrape_toi_news()
    if toi_headlines is not None:
        print(toi_headlines)