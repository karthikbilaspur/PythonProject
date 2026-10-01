import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
import webbrowser
import pandas as pd
from typing import Any, cast
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

class AmazonProductTracker:
    def __init__(self, root: tk.Misc) -> None:
        self.root = root
        self.root.title("Amazon Product Tracker")
        self.product_url = tk.StringVar()
        self.product_name = tk.StringVar()
        self.product_price = tk.StringVar()

        # Create GUI components
        self.create_widgets()

    def create_widgets(self) -> None:
        # Product URL label and entry
        tk.Label(self.root, text="Product URL:").grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.product_url, width=50).grid(row=0, column=1)

        # Track product button
        tk.Button(self.root, text="Track Product", command=self.track_product).grid(row=1, column=0, columnspan=2)

        # Product name label
        tk.Label(self.root, text="Product Name:").grid(row=2, column=0)
        tk.Label(self.root, textvariable=self.product_name).grid(row=2, column=1)

        # Product price label
        tk.Label(self.root, text="Product Price:").grid(row=3, column=0)
        tk.Label(self.root, textvariable=self.product_price).grid(row=3, column=1)

        # Predict price button
        tk.Button(self.root, text="Predict Price", command=self.predict_price).grid(row=4, column=0, columnspan=2)

    def track_product(self) -> None:
        # Send HTTP request to Amazon
        url = self.product_url.get()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract product name and price
        name_element = soup.find('span', {'id': 'productTitle'})
        price_element = soup.find('span', {'id': 'priceblock_ourprice'})
        if name_element is None or price_element is None:
            raise ValueError("Product name or price was not found on the page.")
        product_name = name_element.get_text(strip=True)
        product_price = price_element.get_text(strip=True)

        # Update GUI
        self.product_name.set(product_name)
        self.product_price.set(product_price)

        # Open product page in browser
        webbrowser.open(url)

    def predict_price(self) -> None:
        # Get historical price data
        historical_prices = self.get_historical_prices()

        # Create and train a linear regression model
        model: Any = LinearRegression()
        X = pd.DataFrame(range(len(historical_prices)), columns=['Day'])
        y = pd.DataFrame(historical_prices, columns=['Price'])
        split = cast(Any, train_test_split)
        X_train, X_test, y_train, y_test = split(
            X, y, test_size=0.2, random_state=42
        )
        model.fit(X_train, y_train)

        # Make predictions
        predicted_price: Any = model.predict(X_test)

        # Evaluate model performance
        mse = cast(Any, mean_squared_error)(y_test, predicted_price)
        rmse = mse ** 0.5

        # Display predicted price
        messagebox.showinfo("Predicted Price", f"Predicted price: ${predicted_price[-1][0]:.2f}")
        messagebox.showinfo("Model Performance", f"RMSE: {rmse:.2f}")

    def get_historical_prices(self) -> list[float]:
        # Simulate historical price data
        historical_prices = [10.99, 11.99, 12.99, 13.99, 14.99]
        return historical_prices

if __name__ == "__main__":
    root = tk.Tk()
    app = AmazonProductTracker(root)
    root.mainloop()