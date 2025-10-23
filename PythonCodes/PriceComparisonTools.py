import requests
from bs4 import BeautifulSoup
import sqlite3
from tabulate import tabulate
import pandas as pd

# Database setup
conn = sqlite3.connect('price_comparison.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price REAL,
        website TEXT,
        product_url TEXT
    )
''')

# Function to scrape Amazon
def scrape_amazon(item):
    url = f'https://www.amazon.in/s?k={item.replace(" ", "+")}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error scraping Amazon: {e}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('div', {'class': 's-result-item'})
    data = []
    for product in products:
        try:
            name = product.find('span', {'class': 'a-size-medium'}).text.strip()
            price = product.find('span', {'class': 'a-price-whole'}).text.strip().replace(',', '')
            product_url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal'})['href']
            data.append({
                'name': name,
                'price': float(price),
                'website': 'Amazon',
                'product_url': product_url
            })
        except AttributeError:
            continue
    return data

# Function to scrape Flipkart
def scrape_flipkart(item):
    url = f'https://www.flipkart.com/search?q={item.replace(" ", "%20")}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error scraping Flipkart: {e}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('div', {'class': '_3wU53n'})
    data = []
    for product in products:
        try:
            name = product.text.strip()
            price = product.find_next('div', {'class': '_1vC4OE'}).text.strip().replace(',', '')
            product_url = 'https://www.flipkart.com' + product.find_previous('a')['href']
            data.append({
                'name': name,
                'price': float(price),
                'website': 'Flipkart',
                'product_url': product_url
            })
        except AttributeError:
            continue
        except ValueError:
            continue
    return data

# Function to scrape Snapdeal
def scrape_snapdeal(item):
    url = f'https://www.snapdeal.com/search?keyword={item.replace(" ", "+")}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error scraping Snapdeal: {e}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('p', {'class': 'product-title'})
    data = []
    for product in products:
        try:
            name = product.text.strip()
            price = product.find_next('span', {'class': 'lfloat product-price'}).text.strip().replace(',', '')
            product_url = product.find_previous('a')['href']
            data.append({
                'name': name,
                'price': float(price),
                'website': 'Snapdeal',
                'product_url': product_url
            })
        except AttributeError:
            continue
        except ValueError:
            continue
    return data

# Main function
def main():
    item = input('Enter the item you want to search for: ')
    amazon_data = scrape_amazon(item)
    flipkart_data = scrape_flipkart(item)
    snapdeal_data = scrape_snapdeal(item)
    data = amazon_data + flipkart_data + snapdeal_data
    if data:
        df = pd.DataFrame(data)
        df = df.sort_values(by='price')
        print(tabulate(df, headers='keys', tablefmt='psql'))
        df.to_sql('products', conn, if_exists='replace', index=False)
    else:
        print("No products found.")

if __name__ == '__main__':
    main()