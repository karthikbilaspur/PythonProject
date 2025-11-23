import requests
from bs4 import BeautifulSoup

# Send a GET request to the website
url = "https://books.toscrape.com/"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the book titles and prices on the page
    book_titles = soup.find_all('h3')
    book_prices = soup.find_all('p', class_='price_color')

    # Print the book titles and prices
    for title, price in zip(book_titles, book_prices):
        print(f"Title: {title.text.strip()}")
        print(f"Price: {price.text.strip()}")
        print("-" * 50)
else:
    print("Failed to retrieve the webpage")