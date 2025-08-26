import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

class LinkFetcher:
    def __init__(self, url):
        self.url = url
        self.links = set()
        self.internal_links = set()
        self.external_links = set()
        self.invalid_links = set()

    def fetch_links(self):
        try:
            # Send a GET request
            response = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0'})
            
            # Check if the request was successful
            if response.status_code != 200:
                print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
                return
            
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all links on the webpage
            for link in soup.find_all('a'):
                href = link.get('href')
                
                # Ignore empty or None href attributes
                if not href:
                    continue
                
                # Convert relative URLs to absolute URLs
                href = urljoin(self.url, href)
                
                # Remove any URL fragments
                parsed_href = urlparse(href)
                href = f"{parsed_href.scheme}://{parsed_href.netloc}{parsed_href.path}"
                
                # Check if the link is internal or external
                if self.is_internal_link(href):
                    self.internal_links.add(href)
                elif self.is_valid_link(href):
                    self.external_links.add(href)
                else:
                    self.invalid_links.add(href)
                
                self.links.add(href)
            
            print(f"Total links: {len(self.links)}")
            print(f"Internal links: {len(self.internal_links)}")
            print(f"External links: {len(self.external_links)}")
            print(f"Invalid links: {len(self.invalid_links)}")
        
        except Exception as e:
            print(f"An error occurred: {e}")

    def is_internal_link(self, link):
        return urlparse(link).netloc == urlparse(self.url).netloc

    def is_valid_link(self, link):
        return bool(re.match(r"^https?://[^/]+.*$", link))

    def get_links(self):
        return self.links

    def get_internal_links(self):
        return self.internal_links

    def get_external_links(self):
        return self.external_links

    def get_invalid_links(self):
        return self.invalid_links

# Usage
url = "http://example.com"
fetcher = LinkFetcher(url)
fetcher.fetch_links()

print("\nAll Links:")
for link in fetcher.get_links():
    print(link)

print("\nInternal Links:")
for link in fetcher.get_internal_links():
    print(link)

print("\nExternal Links:")
for link in fetcher.get_external_links():
    print(link)

print("\nInvalid Links:")
for link in fetcher.get_invalid_links():
    print(link)