import feedparser
import requests
from bs4 import BeautifulSoup
import csv

class GoogleNewsScraper:
    def __init__(self, query):
        self.query = query
        self.rss_url = f'https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
        }

    def scrape_rss(self):
        feed = feedparser.parse(self.rss_url)
        news_data = []
        for entry in feed.entries:
            news_data.append({
                'title': entry.title,
                'link': entry.link,
                'published': entry.published
            })
        return news_data

    def scrape_html(self):
        url = f'https://www.google.com/search?q={self.query}&gl=us&tbm=nws&num=100'
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, "html.parser")
        news_tags = soup.find_all('div', class_='MBeuO')
        news_data = []
        for news_tag in news_tags:
            title = news_tag.get_text()
            news_data.append({
                'title': title
            })
        return news_data

    def save_to_csv(self, news_data, filename):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['title', 'link', 'published']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for news in news_data:
                writer.writerow(news)

def main():
    query = input("Enter your search query: ")
    scraper = GoogleNewsScraper(query)
    news_data = scraper.scrape_rss()
    scraper.save_to_csv(news_data, 'news_data.csv')
    print("News data saved to news_data.csv")

if __name__ == '__main__':
    main()