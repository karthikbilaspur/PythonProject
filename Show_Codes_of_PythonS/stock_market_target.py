import tkinter as tk
from tkinter import ttk
import requests
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from typing import Optional, cast

# Alpha Vantage API Key
API_KEY = 'YOUR_API_KEY'

class StockTraderAgent:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title('Stock Market Trader Agent')

        # Create GUI components
        self.stock_label = tk.Label(root, text='Stock Symbol:')
        self.stock_label.pack()

        self.stock_entry = tk.Entry(root)
        self.stock_entry.pack()

        self.fetch_button = tk.Button(root, text='Fetch Data', command=self.fetch_data)
        self.plot_button = tk.Button(root, text='Plot Data', command=self.plot_data)
        self.plot_button.pack()

        self.data: Optional[pd.DataFrame] = None

    def fetch_data(self):
        stock_symbol = self.stock_entry.get()
        ts = TimeSeries(key=API_KEY, output_format='pandas')
        df, _, meta_data = ts.get_daily_adjusted(symbol=stock_symbol, outputsize='full')
        # Cast to a known pandas DataFrame so type checkers know the concrete type
        self.data = cast(pd.DataFrame, df)
        print(self.data.head())

    def plot_data(self):
        if self.data is not None:
            self.data['4. close'].plot()
            plt.title('Stock Price')
            plt.xlabel('Date')
            plt.ylabel('Price')
            plt.show()
        else:
            print('No data fetched')

if __name__ == '__main__':
    root = tk.Tk()
    app = StockTraderAgent(root)
    root.mainloop()