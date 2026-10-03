import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup

class PriceComparator:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Price Comparator")

        self.product_name = tk.StringVar()
        self.product_name_label = tk.Label(root, text="Product Name:")
        self.product_name_label.pack()
        self.product_name_entry = tk.Entry(root, textvariable=self.product_name)
        self.product_name_entry.pack()

        self.search_button = tk.Button(root, text="Search", command=self.search_product)
        self.search_button.pack()

        self.result_text = tk.Text(root)
        self.result_text.pack()

    def scrape_amazon(self, product_name: str) -> list[dict]:
        url = f'https://www.amazon.in/s?k={product_name.replace(" ", "+")}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        products = soup.find_all('div', {'class': 's-result-item'})
        data = []
        for product in products:
            try:
                name = product.find('span', {'class': 'a-size-medium'}).text.strip()
                price = product.find('span', {'class': 'a-price-whole'}).text.strip().replace(',', '')
                data.append({'name': name, 'price': float(price), 'website': 'Amazon'})
            except AttributeError:
                continue
        return data

    def scrape_flipkart(self, product_name: str) -> list[dict]:
        url = f'https://www.flipkart.com/search?q={product_name.replace(" ", "%20")}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        products = soup.find_all('div', {'class': '_3wU53n'})
        data = []
        for product in products:
            try:
                name = product.text.strip()
                price = product.find_next('div', {'class': '_1vC4OE'}).text.strip().replace(',', '')
                data.append({'name': name, 'price': float(price), 'website': 'Flipkart'})
            except AttributeError:
                continue
        return data

    def search_product(self):
        product_name = self.product_name.get()
        amazon_data = self.scrape_amazon(product_name)
        flipkart_data = self.scrape_flipkart(product_name)
        data = amazon_data + flipkart_data
        data.sort(key=lambda x: x['price'])
        self.result_text.delete('1.0', tk.END)
        for product in data:
            self.result_text.insert(tk.END, f"Name: {product['name']}\nPrice: {product['price']}\nWebsite: {product['website']}\n\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = PriceComparator(root)
    root.mainloop()