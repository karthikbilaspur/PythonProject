import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def scrape_website(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def parse_html(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    except Exception as e:
        print(f"An error occurred while parsing HTML: {e}")
        return None

def extract_data(soup):
    try:
        # Replace with your own logic to extract the data you need
        titles = soup.find_all(['h1', 'h2', 'h3'])
        links = soup.find_all('a')
        data = {
            'titles': [title.text.strip() for title in titles],
            'links': [link.get('href') for link in links if link.get('href')]
        }
        return data
    except Exception as e:
        print(f"An error occurred while extracting data: {e}")
        return None

def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def main():
    while True:
        url = input("Enter the URL of the website to scrape (or 'q' to quit): ")
        if url.lower() == 'q':
            break
        if not validate_url(url):
            print("Invalid URL. Please try again.")
            continue
        html = scrape_website(url)
        if html:
            soup = parse_html(html)
            if soup:
                data = extract_data(soup)
                if data:
                    print("Extracted Data:")
                    print("Titles:")
                    for title in data['titles']:
                        print(title)
                    print("\nLinks:")
                    for link in data['links']:
                        print(link)

if __name__ == "__main__":
    main()