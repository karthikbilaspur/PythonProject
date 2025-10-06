
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys

class ImageScraper:
    def __init__(self, url):
        self.url = url
        self.images = []

    def scrape_images(self):
        try:
            response = requests.get(self.url, headers=self.get_headers())
            response.raise_for_status()
        except requests.RequestException as e:
            sys.exit(f"Request failed: {e}")

        html_data = BeautifulSoup(response.text, 'html.parser')
        images = html_data.find_all('img', src=True)

        for image in images:
            img_src = image['src']
            if not bool(urlparse(img_src).netloc):
                img_src = urljoin(self.url, img_src)
            self.images.append(img_src)

    def get_headers(self):
        return {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        }

    def print_images(self):
        for image in self.images:
            print(image)

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python scrape_images.py {url}")
    scraper = ImageScraper(sys.argv[1])
    scraper.scrape_images()
    scraper.print_images()

if __name__ == "__main__":
    main()