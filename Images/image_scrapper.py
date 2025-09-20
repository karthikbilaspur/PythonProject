from bs4 import BeautifulSoup
import requests
import sys
from urllib.parse import urljoin, urlparse

def scrape_images(url):
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
            }
        )
        response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
    except requests.RequestException as e:
        sys.exit(f"Request failed: {e}")

    html_data = BeautifulSoup(response.text, 'html.parser')
    images = html_data.find_all('img', src=True)

    for image in images:
        img_src = image['src']
        if not bool(urlparse(img_src).netloc):
            img_src = urljoin(url, img_src)
        print(img_src)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python scrape_images.py {url}")
    scrape_images(sys.argv[1])