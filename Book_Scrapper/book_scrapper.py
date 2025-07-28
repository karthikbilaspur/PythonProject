import requests
from bs4 import BeautifulSoup
import csv

def scrape_books(url, category=None):
    book_data = []
    if category:
        categories = [category]
    else:
        categories = get_categories(url)

    for category in categories:
        page = 1
        while True:
            try:
                page_url = f'{url}/catalogue/category/books/{category}/page-{page}.html'
                response = requests.get(page_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                books = soup.find_all('article', class_='product_pod')
                if not books:
                    break
                for book in books:
                    book_info = extract_book_info(url, book)
                    book_data.append(book_info)
                page += 1
            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break

    return book_data

def get_categories(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    categories = [li.a['href'].split('/')[3] for li in soup.find('ul', class_='nav nav-list').find('ul').find_all('li')]
    return categories

def extract_book_info(url, book):
    title = book.find('h3').text
    price = book.find('p', class_='price_color').text
    rating = book.find('p', class_='star-rating')['class'][1]
    book_url = book.find('a')['href']
    book_response = requests.get(f'{url}/catalogue/{book_url[9:]}')
    book_soup = BeautifulSoup(book_response.content, 'html.parser')
    description = book_soup.find('meta', attrs={'name': 'description'})['content']
    return {
        'title': title,
        'price': price,
        'rating': rating,
        'description': description
    }

def save_to_csv(book_data, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['title', 'price', 'rating', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for book in book_data:
            writer.writerow(book)

def main():
    url = 'http://books.toscrape.com'
    category = input("Enter a category (or leave blank for all categories): ")
    if category:
        book_data = scrape_books(url, category)
        filename = f'{category}_books.csv'
    else:
        book_data = scrape_books(url)
        filename = 'all_books.csv'
    save_to_csv(book_data, filename)
    print(f'Book data saved to {filename}')

if __name__ == '__main__':
    main()