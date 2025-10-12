import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Categories and their URL slugs
most_active = {'Most Active equities - Main Board': 'mae_mainboard_tableC', 
               'Most Active equities - SME': 'mae_sme_tableC', 
               'Most Active equities - ETFs': 'mae_etf_tableC',
               'Most Active equities - Price Spurts': 'mae_pricespurts_tableC', 
               'Most Active equities - Volume Spurts': 'mae_volumespurts_tableC'}
top_20 = {'NIFTY 50 Top 20 Gainers': 'topgainer-Table',
          'NIFTY 50 Top 20 Losers': 'toplosers-Table'}

class NSEStockData:
    def __init__(self, root):
        self.root = root
        self.root.title('NSE Stock data')
        self.root.geometry('1200x1000')
        self.root.configure(bg='white')
        
        self.driver_path = tk.StringVar()
        self.category = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # label text for title
        ttk.Label(self.root, text="NSE Stock market data",
                  background='white', foreground="SpringGreen2",
                  font=("Helvetica", 30, 'bold')).grid(row=0, column=1)

        # label
        ttk.Label(self.root, text="Enter path for chromedriver:", 
                  background='white', font=("Helvetica", 15)).grid(column=0, row=1, padx=10, pady=25)
        tk.Entry(self.root, textvariable=self.driver_path, width=50).grid(column=1, row=1)

        ttk.Label(self.root, text="Select Market data to get:", background='white',
                  font=("Helvetica", 15)).grid(column=0, row=2, padx=10, pady=25)

        # Combobox creation
        self.category_combo = ttk.Combobox(self.root, textvariable=self.category, width=60, state='readonly', font="Helvetica 15")
        self.category_combo['values'] = list(most_active.keys()) + list(top_20.keys())
        self.category_combo.current(0)
        self.category_combo.grid(column=1, row=2, padx=10)

        submit_btn = ttk.Button(self.root, text="Get Stock Data!", command=self.scraper)
        submit_btn.grid(row=2, column=3, pady=5, padx=15, ipadx=5)

        self.query_label = tk.Text(self.root, height="52", width="500", bg="alice blue")
        self.query_label.grid(row=3, column=0, columnspan=4)

    def generate_url(self):
        category_choice = self.category.get()
        if category_choice in most_active:
            page = 'most-active-equities'
        else:
            page = 'top-gainers-loosers'
        url = 'https://www.nseindia.com/market-data/{}'.format(page)
        return url

    def scraper(self):
        driver_path = self.driver_path.get()
        if not driver_path:
            self.query_label.delete(1.0, "end")
            self.query_label.insert(1.0, "Please enter the path for chromedriver")
            return

        url = self.generate_url()
        driver = webdriver.Chrome(driver_path)
        driver.get(url)

        # Wait for results to load
        time.sleep(5)
        html = driver.page_source

        # Start scraping resultant html data
        soup = BeautifulSoup(html, 'html.parser')

        # Based on choice scrape div
        category_choice = self.category.get()
        if category_choice in most_active:
            category_div = most_active[category_choice]
        else:
            category_div = top_20[category_choice]

        # Find the table to scrape
        results = soup.find("table", {"id": category_div})
        rows = results.findChildren('tr')

        table_data = []
        row_values = []
        # Append stock data into a list
        for row in rows:
            cells = row.findChildren(['th', 'td'])
            for cell in cells:
                value = cell.text.strip()
                value = " ".join(value.split())
                row_values.append(value)
            table_data.append(row_values)
            row_values = []

        # Formatting the stock data stored in the list
        stocks_data = ""
        for stock in table_data:
            single_record = ""
            for cell in stock:
                format_cell = "{:<20}"
                single_record += format_cell.format(cell[:20])
            single_record += "\n"
            stocks_data += single_record

        # Adding the formatted data into tkinter GUI
        self.query_label.delete(1.0, "end")
        self.query_label.insert(1.0, stocks_data)
        driver.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = NSEStockData(root)
    root.mainloop()