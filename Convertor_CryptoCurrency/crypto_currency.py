
import requests

class CryptoConverter:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"

    def get_crypto_price(self, crypto_id):
        response = requests.get(f"{self.base_url}/coins/{crypto_id}?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false")
        if response.status_code == 200:
            return response.json()['market_data']['current_price']
        else:
            return None

    def get_crypto_list(self):
        response = requests.get(f"{self.base_url}/coins/list")
        if response.status_code == 200:
            return response.json()
        else:
            return []

    def convert_crypto(self, from_crypto, to_crypto, amount):
        from_price = self.get_crypto_price(from_crypto)
        to_price = self.get_crypto_price(to_crypto)
        if from_price and to_price:
            from_usd = from_price['usd']
            to_usd = to_price['usd']
            result = (amount * from_usd) / to_usd
            return result
        else:
            return None

    def get_crypto_info(self, crypto_id):
        response = requests.get(f"{self.base_url}/coins/{crypto_id}?localization=false&tickers=false&market_data=true&community_data=true&developer_data=false&sparkline=false")
        if response.status_code == 200:
            return response.json()
        else:
            return None

def main():
    converter = CryptoConverter()
    print("Cryptocurrency Converter")
    while True:
        print("\n1. Convert cryptocurrency")
        print("2. Get cryptocurrency price")
        print("3. Get cryptocurrency list")
        print("4. Get cryptocurrency info")
        print("5. Quit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            from_crypto = input("Enter the cryptocurrency to convert from (e.g., bitcoin): ").lower()
            to_crypto = input("Enter the cryptocurrency to convert to (e.g., ethereum): ").lower()
            amount = float(input("Enter the amount: "))
            result = converter.convert_crypto(from_crypto, to_crypto, amount)
            if result:
                print(f"{amount} {from_crypto} is equal to {result} {to_crypto}")
            else:
                print("Failed to convert cryptocurrency")
        elif choice == "2":
            crypto_id = input("Enter the cryptocurrency (e.g., bitcoin): ").lower()
            price = converter.get_crypto_price(crypto_id)
            if price:
                print(f"Current price of {crypto_id}: ${price['usd']}")
            else:
                print("Failed to get cryptocurrency price")
        elif choice == "3":
            crypto_list = converter.get_crypto_list()
            if crypto_list:
                for crypto in crypto_list[:10]:  # Show first 10 cryptocurrencies
                    print(f"{crypto['name']} ({crypto['symbol']}) - {crypto['id']}")
            else:
                print("Failed to get cryptocurrency list")
        elif choice == "4":
            crypto_id = input("Enter the cryptocurrency (e.g., bitcoin): ").lower()
            crypto_info = converter.get_crypto_info(crypto_id)
            if crypto_info:
                print(f"Name: {crypto_info['name']}")
                print(f"Symbol: {crypto_info['symbol']}")
                print(f"Current Price: ${crypto_info['market_data']['current_price']['usd']}")
                print(f"Market Cap: ${crypto_info['market_data']['market_cap']['usd']}")
            else:
                print("Failed to get cryptocurrency info")
        elif choice == "5":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
