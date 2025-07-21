import requests
from bs4 import BeautifulSoup

def scrape_ubuntu_news():
    url = "https://ubuntu.com/blog"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_articles = soup.find_all('article')

    for article in news_articles:
        title = article.find('h2').text.strip()
        link = article.find('a')['href']
        print(f"Title: {title}")
        print(f"Link: {link}")
        print()

def scrape_ubuntu_downloads():
    url = "https://ubuntu.com/download"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    download_links = soup.find_all('a', class_='download-link')

    for link in download_links:
        print(f"Download Link: {link['href']}")

def main():
    while True:
        print("Ubuntu Scraper Menu:")
        print("1. Scrape News")
        print("2. Scrape Downloads")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            scrape_ubuntu_news()
        elif choice == "2":
            scrape_ubuntu_downloads()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()