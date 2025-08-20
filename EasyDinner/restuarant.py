class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

class Restaurant:
    def __init__(self):
        self.menu = []
        self.cart = []
        self.orders = []
        self.users = []
        self.logged_in_user = None

    def add_menu_item(self, name, price):
        self.menu.append(MenuItem(name, price))

    def display_menu(self):
        print("Menu:")
        for i, item in enumerate(self.menu, start=1):
            print(f"{i}. {item.name} - ${item.price:.2f}")

    def add_to_cart(self, item_number):
        try:
            item_number = int(item_number)
            if item_number < 1 or item_number > len(self.menu):
                print("Invalid item number.")
                return
            self.cart.append(self.menu[item_number - 1])
            print(f"Added {self.menu[item_number - 1].name} to cart.")
        except ValueError:
            print("Invalid input.")

    def view_cart(self):
        if not self.cart:
            print("Cart is empty.")
            return
        print("Cart:")
        for i, item in enumerate(self.cart, start=1):
            print(f"{i}. {item.name} - ${item.price:.2f}")
        print(f"Total: ${sum(item.price for item in self.cart):.2f}")

    def place_order(self):
        if not self.cart:
            print("Cart is empty.")
            return
        self.orders.append({"order": self.cart[:], "status": "pending", "user": self.logged_in_user.username})
        self.cart.clear()
        print("Order placed successfully.")

    def view_orders(self):
        if not self.orders:
            print("No orders yet.")
            return
        for i, order in enumerate(self.orders, start=1):
            print(f"Order {i}:")
            for j, item in enumerate(order["order"], start=1):
                print(f"{j}. {item.name} - ${item.price:.2f}")
            print(f"Total: ${sum(item.price for item in order['order']):.2f}")
            print(f"Status: {order['status']}")
            print(f"User: {order['user']}")
            print()

    def register_user(self, username, password, role):
        self.users.append(User(username, password, role))

    def login_user(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                self.logged_in_user = user
                print("Login successful.")
                return
        print("Invalid username or password.")

    def admin_panel(self):
        if self.logged_in_user and self.logged_in_user.role == "admin":
            while True:
                print("\n1. Add Menu Item")
                print("2. View Orders")
                print("3. Update Order Status")
                print("4. Exit")

                choice = input("Choose an option: ")

                if choice == "1":
                    name = input("Enter menu item name: ")
                    price = float(input("Enter menu item price: "))
                    self.add_menu_item(name, price)
                elif choice == "2":
                    self.view_orders()
                elif choice == "3":
                    order_number = int(input("Enter order number: ")) - 1
                    if order_number < 0 or order_number >= len(self.orders):
                        print("Invalid order number.")
                        continue
                    status = input("Enter new status: ")
                    self.orders[order_number]["status"] = status
                elif choice == "4":
                    break
                else:
                    print("Invalid option.")
        else:
            print("Access denied.")

def main():
    restaurant = Restaurant()

    # Adding menu items
    restaurant.add_menu_item("Burger", 10.99)
    restaurant.add_menu_item("Fries", 4.99)
    restaurant.add_menu_item("Soda", 2.99)

    # Registering users
    restaurant.register_user("admin", "password", "admin")
    restaurant.register_user("user", "password", "user")

    while True:
        if not restaurant.logged_in_user:
            print("\n1. Login")
            print("2. Register")
            print("3. Exit")

            choice = input("Choose an option: ")

            if choice == "1":
                username = input("Enter username: ")
                password = input("Enter password: ")
                restaurant.login_user(username, password)
            elif choice == "2":
                username = input("Enter username: ")
                password = input("Enter password: ")
                role = input("Enter role (admin/user): ")
                restaurant.register_user(username, password, role)
            elif choice == "3":
                break
            else:
                print("Invalid option.")
        else:
            if restaurant.logged_in_user.role == "admin":
                print("\n1. Display Menu")
                print("2. Add to Cart")
                print("3. View Cart")
                print("4. Place Order")
                print("5. View Orders")
                print("6. Admin Panel")
                print("7. Logout")

                choice = input("Choose an option: ")

                if choice == "1":
                    restaurant.display_menu()
                elif choice == "2":
                    restaurant.display_menu()
                    item_number = input("Enter item number to add to cart: ")
                    restaurant.add_to_cart(item_number)
                elif choice == "3":
                    restaurant.view_cart()
                elif choice == "4":
                    restaurant.place_order()
                elif choice == "5":
                    restaurant.view_orders()
                elif choice == "6":
                    restaurant.admin_panel()
                elif choice == "7":
                    restaurant.logged_in_user = None
                else:
                    print("Invalid option.")
            else:
                print("\n1. Display Menu")
                print("2. Add to Cart")
                print("3. View Cart")
                print("4. Place Order")
                print("5. View Orders")
                print("6. Logout")

                choice = input("Choose an option: ")

                if choice == "1":
                    restaurant.display_menu()
                elif choice == "2":
                    restaurant.display_menu()
                    item_number = input("Enter item number to add to cart: ")
                    restaurant.add_to_cart(item_number)
                elif choice == "3":
                    restaurant.view_cart()
                elif choice == "4":
                    restaurant.place_order()
                elif choice == "5":
                    restaurant.view_orders()
                elif choice == "6":
                    restaurant.logged_in_user = None
                else:
                    print("Invalid option.")

if __name__ == "__main__":
    main()