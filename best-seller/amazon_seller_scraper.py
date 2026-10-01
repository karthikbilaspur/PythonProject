import random
import time
from typing import Optional

import requests
from bs4 import BeautifulSoup


def scrape_amazon_best_sellers(category_url: str) -> list[dict[str, Optional[str]]]:
    # Set User-Agent rotation
    user_agents: list[str] = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        # Add more User-Agent strings here
    ]

    # Set rate limiting
    delay: float = random.uniform(1, 3)  # Random delay between 1-3 seconds

    headers = {'User-Agent': random.choice(user_agents)}
    try:
        response = requests.get(category_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return []

    soup = BeautifulSoup(response.text, 'lxml')

    # Extract product data
    products = soup.find_all('div', class_='zg-item')

    product_data: list[dict[str, Optional[str]]] = []
    for product in products:
        try:
            title_element = product.find('a', class_='a-link-normal')
            if title_element:
                title = title_element.get_text(strip=True)
                href = title_element.get('href')
                url = f'https://www.amazon.com{href}' if href else None
            else:
                title = None
                url = None

            price_element = product.find('span', class_='p13n-sc-price')
            if price_element:
                price = price_element.get_text(strip=True)
            else:
                price = None

            rating_element = product.find('span', class_='a-icon-alt')
            if rating_element:
                rating = rating_element.get_text(strip=True)
            else:
                rating = None

            reviews_element = product.find('a', class_='a-size-small a-link-normal')
            if reviews_element:
                reviews = reviews_element.get_text(strip=True)
            else:
                reviews = None

            product_data.append({
                'title': title,
                'url': url,
                'price': price,
                'rating': rating,
                'reviews': reviews
            })
        except Exception as e:
            print(f"Error parsing product: {e}")

        # Rate limiting
        time.sleep(delay)

    return product_data