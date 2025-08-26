import requests
import json
import base64
from getpass import getpass

class FlipkartAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self.get_access_token()

    def get_access_token(self):
        # Generate access token using Client Credentials Flow
        url = "https://api.flipkart.net/oauth-service/oauth/token"
        params = {"grant_type": "client_credentials", "scope": "Seller_Api"}
        headers = {"Authorization": f"Basic {self.get_base64_encoded_string()}"}
        response = requests.get(url, params=params, headers=headers)
        return response.json()["access_token"]

    def get_base64_encoded_string(self):
        # Base64 encode client ID and client secret
        return base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()

    def get_products(self, category):
        # Fetch products using Product Feed API
        url = f"https://affiliate-api.flipkart.net/affiliate/feeds/{self.client_id}/category/{category}.json"
        headers = {"Fk-Affiliate-Id": self.client_id, "Fk-Affiliate-Token": self.client_secret}
        response = requests.get(url, headers=headers)
        return response.json()

    def search_products(self, query):
        # Search products using Search Query API
        url = f"https://affiliate-api.flipkart.net/affiliate/1.0/search.json?query={query}"
        headers = {"Fk-Affiliate-Id": self.client_id, "Fk-Affiliate-Token": self.client_secret}
        response = requests.get(url, headers=headers)
        return response.json()

    def get_orders(self):
        # Fetch orders using Order Management API
        url = "https://api.flipkart.net/sellers/v3/shipments/filter"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.post(url, headers=headers)
        return response.json()

    def update_inventory(self, sku_id, quantity):
        # Update inventory using Inventory Management API
        url = f"https://api.flipkart.net/sellers/skus/{sku_id}/listings"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        data = {"attributeValues": {"inventory": quantity}}
        response = requests.put(url, headers=headers, json=data)
        return response.json()

def main():
    client_id = input("Enter your client ID: ")
    client_secret = getpass("Enter your client secret: ")
    flipkart_api = FlipkartAPI(client_id, client_secret)

    while True:
        print("1. Get products")
        print("2. Search products")
        print("3. Get orders")
        print("4. Update inventory")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            category = input("Enter the category (e.g., electronics): ")
            products = flipkart_api.get_products(category)
            print(json.dumps(products, indent=4))
        elif choice == "2":
            query = input("Enter your search query (e.g., apple watch): ")
            search_results = flipkart_api.search_products(query)
            print(json.dumps(search_results, indent=4))
        elif choice == "3":
            orders = flipkart_api.get_orders()
            print(json.dumps(orders, indent=4))
        elif choice == "4":
            sku_id = input("Enter the SKU ID: ")
            quantity = int(input("Enter the quantity: "))
            inventory_update = flipkart_api.update_inventory(sku_id, quantity)
            print(json.dumps(inventory_update, indent=4))
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()