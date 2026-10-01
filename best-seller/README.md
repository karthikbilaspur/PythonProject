# Amazon Best Seller Scraper

A Python script that scrapes Amazon Best Sellers pages and extracts product data.

## Features

* **Product Data Extraction**: Extracts title, URL, price, rating, and reviews for each product.
* **User-Agent Rotation**: Rotates User-Agent headers to avoid being blocked by Amazon.
* **Rate Limiting**: Adds a random delay between requests to avoid overwhelming Amazon's servers.
* **Error Handling**: Handles potential errors during requests and HTML parsing.

## Requirements

* **Python 3.x**: Required to run the script.
* **requests**: Required for making HTTP requests to Amazon.
* **BeautifulSoup**: Required for parsing HTML responses.

## Installation

1. Install Python 3.x if you haven't already.
2. Install the required libraries using pip:
```bash
pip install requests beautifulsoup4