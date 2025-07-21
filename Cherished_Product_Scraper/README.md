A Python-based Amazon product scraper that extracts product information, images, and customer reviews.

## Features

* **Product Information Extraction**: Extracts product details such as name, price, rating, and more.
* **Product Image Extraction**: Extracts product images from Amazon product pages.
* **Customer Review Extraction**: Extracts customer reviews from Amazon product pages.
* **Rate Limiting**: Implements rate limiting to avoid overwhelming Amazon's servers.
* **User-Agent Rotation**: Rotates User-Agent strings to avoid being blocked by Amazon.

## Requirements

* **Python 3.x**: Required to run the script.
* **requests**: Required for sending HTTP requests to Amazon.
* **BeautifulSoup**: Required for parsing HTML content.
* **fake-useragent**: Required for rotating User-Agent strings.
* **ratelimit**: Required for implementing rate limiting.

## Installation

1. Install Python 3.x if you haven't already.
2. Install the required libraries using pip:
```bash
pip install requests beautifulsoup4 fake-useragent ratelimit