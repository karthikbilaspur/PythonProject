import requests
import json
import matplotlib.pyplot as plt
import time

class BitcoinTracker:
    def __init__(self, api_url):
        self.api_url = api_url
        self.prices = []

    def get_bitcoin_price(self):
        response = requests.get(self.api_url)
        data = json.loads(response.content)
        price = data["bpi"]["USD"]["rate"]
        return price.replace(",", "")

    def track_price(self, interval=60):
        while True:
            price = self.get_bitcoin_price()
            self.prices.append(float(price))
            print(f"Current Bitcoin price: ${price}")
            plt.clf()
            plt.plot(self.prices)
            plt.xlabel("Time")
            plt.ylabel("Price (USD)")
            plt.title("Bitcoin Price")
            plt.pause(0.01)
            time.sleep(interval)

    def plot_prices(self):
        plt.plot(self.prices)
        plt.xlabel("Time")
        plt.ylabel("Price (USD)")
        plt.title("Bitcoin Price")
        plt.show()

def main():
    api_url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    tracker = BitcoinTracker(api_url)
    tracker.track_price()

if __name__ == "__main__":
    main()