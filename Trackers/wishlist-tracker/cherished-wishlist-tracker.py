import json
import os

class AmazonWishlist:
    def __init__(self, filename="wishlist.json"):
        self.filename = filename
        self.wishlist = self.load_wishlist()

    def load_wishlist(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                return json.load(file)
        else:
            return {}

    def save_wishlist(self):
        with open(self.filename, "w") as file:
            json.dump(self.wishlist, file, indent=4)

    def add_item(self, item_name: str, price: float, link: str = "", product_id: str = "") -> None:
        """Add an item to the Amazon wishlist."""
        self.wishlist[item_name] = {
            "price": price,
            "link": link,
            "product_id": product_id,
        }
        self.save_wishlist()
        print(f"Item '{item_name}' added to Amazon wishlist.")

    def remove_item(self, item_name: str) -> None:
        """Remove an item from the Amazon wishlist."""
        if item_name in self.wishlist:
            del self.wishlist[item_name]
            self.save_wishlist()
            print(f"Item '{item_name}' removed from Amazon wishlist.")
        else:
            print(f"Item '{item_name}' not found in Amazon wishlist.")

    def view_wishlist(self) -> None:
        """View all items in the Amazon wishlist."""
        if not self.wishlist:
            print("Amazon wishlist is empty.")
        else:
            for item, details in self.wishlist.items():
                print(f"Item: {item}")
                print(f"Price: ${details['price']:.2f}")
                print(f"Link: {details['link']}")
                print()

    def search_item(self, item_name: str) -> None:
        """Search for an item in the Amazon wishlist."""
        if item_name in self.wishlist:
            item_details = self.wishlist[item_name]
            print(f"Item: {item_name}")
            print(f"Price: ${item_details['price']:.2f}")
            print(f"Link: {item_details['link']}")
        else:
            print(f"Item '{item_name}' not found in Amazon wishlist.")

    def track_price(self, item_name: str) -> None:
        """Track the price of an item in the Amazon wishlist."""
        if item_name in self.wishlist:
            current_price = self.wishlist[item_name]["price"]
            print(f"Current price of {item_name}: ${current_price:.2f}")
        else:
            print(f"Item '{item_name}' not found in Amazon wishlist.")

    def update_price(self, item_name: str, new_price: float) -> None:
        """Update the price of an item in the Amazon wishlist."""
        if item_name in self.wishlist:
            self.wishlist[item_name]["price"] = new_price
            self.save_wishlist()
            print(f"Price of {item_name} updated to ${new_price:.2f}")
        else:
            print(f"Item '{item_name}' not found in Amazon wishlist.")

def main():
    amazon_wishlist = AmazonWishlist()
    while True:
        print("\nAmazon Wishlist Menu:")
        print("1. Add item to Amazon wishlist")
        print("2. Remove item from Amazon wishlist")
        print("3. View Amazon wishlist")
        print("4. Search for an item")
        print("5. Track price of an item")
        print("6. Update price of an item")
        print("7. Quit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            item_name = input("Enter item name: ")
            price = float(input("Enter item price: "))
            link = input("Enter item link (optional): ")
            product_id = input("Enter product ID (optional): ")
            if link and product_id:
                amazon_wishlist.add_item(item_name, price, link, product_id)
            elif link:
                amazon_wishlist.add_item(item_name, price, link)
            else:
                amazon_wishlist.add_item(item_name, price)
        elif choice == "2":
            item_name = input("Enter item name: ")
            amazon_wishlist.remove_item(item_name)
        elif choice == "3":
            amazon_wishlist.view_wishlist()
        elif choice == "4":
            item_name = input("Enter item name: ")
            amazon_wishlist.search_item(item_name)
        elif choice == "5":
            item_name = input("Enter item name: ")
            amazon_wishlist.track_price(item_name)
        elif choice == "6":
            item_name = input("Enter item name: ")
            new_price = float(input("Enter new price: "))
            amazon_wishlist.update_price(item_name, new_price)
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()