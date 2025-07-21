import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_amazon_best_sellers(category_url):
    # Set User-Agent rotation
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        # Add more User-Agent strings here
    ]

    # Set rate limiting
    delay = random.uniform(1, 3)  # Random delay between 1-3 seconds

    headers = {'User-Agent': random.choice(user_agents)}
    try:
        response = requests.get(category_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return []

    soup = BeautifulSoup(response.text, 'lxml')

    # Extract product data
    products = soup.find_all('div', {'class': 'zg-item'})

    product_data = []
    for product in products:
        try:
            title_element = product.find('a', {'class': 'a-link-normal'})
            if title_element:
                title = title_element.text.strip()
                url = 'https://www.amazon.com' + title_element['href']
            else:
                title = None
                url = None

            price_element = product.find('span', {'class': 'p13n-sc-price'})
            if price_element:
                price = price_element.text.strip()
            else:
                price = None

            rating_element = product.find('span', {'class': 'a-icon-alt'})
            if rating_element:
                rating = rating_element.text.strip()
            else:
                rating = None

            reviews_element = product.find('a', {'class': 'a-size-small a-link-normal'})
            if reviews_element:
                reviews = reviews_element.text.strip()
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

    return product_data()