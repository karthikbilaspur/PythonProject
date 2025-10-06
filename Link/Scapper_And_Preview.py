import requests
import json
import os
import time
from bs4 import BeautifulSoup

# Function to scrape links
def scrape_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href and href.startswith('http'):  
                print(href)
    except Exception as e:
        print(f"Failed to scrape links: {e}")

# Function to get title
def get_title(soup):
    try:
        og_title = soup.find("meta", property="og:title")
        twitter_title = soup.find("meta", attrs={"name": "twitter:title"})
        document_title = soup.find("title")
        h1_title = soup.find("h1")
        h2_title = soup.find("h2")
        p_title = soup.find("p")

        res = og_title or twitter_title or document_title or h1_title or h2_title or p_title
        res = res.get_text() or res.get("content", None)

        if res and len(res) > 60:
            res = res[0:60]
        if not res or len(res.strip()) == 0:
            res = "Not available"
        return res.strip()
    except Exception as e:
        return "Not available"

# Function to get description
def get_description(soup):
    try:
        og_desc = soup.find("meta", property="og:description")
        twitter_desc = soup.find("meta", attrs={"name": "twitter:description"})
        meta_desc = soup.find("meta", attrs={"name": "description"})
        p_desc = soup.find("p")

        res = og_desc or twitter_desc or meta_desc or p_desc
        res = res.get_text() or res.get("content", None)
        if res and len(res) > 60:
            res = res[0:60]
        if not res or len(res.strip()) == 0:
            res = "Not available"
        return res.strip()
    except Exception as e:
        return "Not available"

# Function to get image
def get_image(soup, url):
    try:
        og_img = soup.find("meta", property="og:image")
        twitter_img = soup.find("meta", attrs={"name": "twitter:image"})
        meta_img = soup.find("link", attrs={"rel": "img_src"})
        img = soup.find("img")

        res = og_img or twitter_img or meta_img or img
        res = res.get("content", None) or res.get_text() or res.get("src", None)

        if res and not res.startswith("http"):
            res = url + "/" + res
        if not res or len(res.strip()) == 0:
            res = "Not available"
        return res
    except Exception as e:
        return "Not available"

# Function to print data
def print_data(data):
    for item in data.items():
        print(f'{item[0].capitalize()}: {item[1]}')

def main():
    url = input("Enter URL: ")
    if not url.startswith("http"):
        url = f"https://{url}"

    scrape_links(url)

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        data = {
            "title": get_title(soup),
            "description": get_description(soup),
            "url": url,
            "image": get_image(soup, url),
        }
        print_data(data)
    except Exception as e:
        print(f"Failed to fetch data: {e}")

if __name__ == "__main__":
    main()