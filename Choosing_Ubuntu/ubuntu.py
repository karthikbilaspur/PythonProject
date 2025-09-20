import requests
from bs4 import BeautifulSoup

def scrape_ubuntu_news(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    news_articles = soup.find_all('article')

    for article in news_articles:
        title = article.find('h2')
        link = article.find('a')
        if title and link:
            print(f"Title: {title.text.strip()}")
            print(f"Link: {link['href']}")
            print()

def scrape_ubuntu_downloads(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    download_links = soup.find_all('a', class_='download-link')

    for link in download_links:
        print(f"Download Link: {link['href']}")

def get_ubuntu_news_url():
    return "https://ubuntu.com/blog"

def get_ubuntu_downloads_url():
    return "https://ubuntu.com/download"

def main():
    news_url = get_ubuntu_news_url()
    downloads_url = get_ubuntu_downloads_url()

    while True:
        print("Ubuntu Scraper Menu:")
        print("1. Scrape News")
        print("2. Scrape Downloads")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            scrape_ubuntu_news(news_url)
        elif choice == "2":
            scrape_ubuntu_downloads(downloads_url)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()