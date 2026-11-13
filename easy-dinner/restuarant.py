from typing import TypedDict


class MenuItem:
    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    def __repr__(self) -> str:
        return f"{self.name} - ${self.price:.2f}"


class User:
    def __init__(self, username: str, password: str, role: str) -> None:
        self.username = username
        self.password = password  # Note: In a real app, hash this!
        self.role = role
        self.cart: list[MenuItem] = []  # Cart now belongs to the user


class Order(TypedDict):
    order: list[MenuItem]
    status: str
    user: str

class Restaurant:
    def __init__(self) -> None:
        self.menu: list[MenuItem] = []
        self.orders: list[Order] = []
        self.users: list[User] = []
        self.logged_in_user: User | None = None

    # --- Menu ---
    def add_menu_item(self, name: str, price: float) -> None:
        if price < 0:
            print("Price cannot be negative.")
            return
        self.menu.append(MenuItem(name, price))
        print(f"Added {name} to menu.")

    def display_menu(self):
        if not self.menu:
            print("Menu is empty.")
            return
        print("Menu:")
        for i, item in enumerate(self.menu, start=1):
            print(f"{i}. {item}")

    # --- Cart ---
    def add_to_cart(self, item_number: str) -> None:
        if self.logged_in_user is None:
            print("Please log in to add items to your cart.")
            return

        try:
            item_index = int(item_number)
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        if item_index < 1 or item_index > len(self.menu):
            print("Invalid item number.")
            return

        item = self.menu[item_index - 1]
        self.logged_in_user.cart.append(item)
        print(f"Added {item.name} to cart.")

    def view_cart(self):
        if self.logged_in_user is None:
            print("Please log in to view your cart.")
            return

        cart = self.logged_in_user.cart
        if not cart:
            print("Cart is empty.")
            return
        print("Cart:")
        for i, item in enumerate(cart, start=1):
            print(f"{i}. {item}")
        print(f"Total: ${sum(item.price for item in cart):.2f}")

    # --- Orders ---
    def place_order(self):
        if self.logged_in_user is None:
            print("Please log in to place an order.")
            return

        cart = self.logged_in_user.cart
        if not cart:
            print("Cart is empty.")
            return
        self.orders.append({
            "order": cart[:],
            "status": "pending",
            "user": self.logged_in_user.username
        })
        cart.clear()
        print("Order placed successfully.")

    def view_orders(self):
        if self.logged_in_user is None:
            print("Please log in to view orders.")
            return

        if not self.orders:
            print("No orders yet.")
            return

        # Admin sees all, user sees only their own
        if self.logged_in_user.role == "admin":
            orders_to_show = list(enumerate(self.orders, start=1))
        else:
            orders_to_show = [(i + 1, o) for i, o in enumerate(self.orders)
                              if o["user"] == self.logged_in_user.username]
            if not orders_to_show:
                print("You have no orders yet.")
                return

        for i, order in orders_to_show:
            print(f"Order {i}:")
            for j, item in enumerate(order["order"], start=1):
                print(f"  {j}. {item}")
            print(f"  Total: ${sum(item.price for item in order['order']):.2f}")
            print(f"  Status: {order['status']}")
            print(f"  User: {order['user']}\n")

    # --- Auth ---
    def register_user(self, username: str, password: str, role: str) -> bool:
        role = role.lower().strip()
        if role not in ("admin", "user"):
            print("Invalid role. Must be 'admin' or 'user'.")
            return False
        if any(u.username == username for u in self.users):
            print("Username already exists.")
            return False
        self.users.append(User(username, password, role))
        print("Registration successful.")
        return True

    def login_user(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                self.logged_in_user = user
                print("Login successful.")
                return True
        print("Invalid username or password.")
        return False

    def logout(self):
        self.logged_in_user = None
        print("Logged out.")

    # --- Admin ---
    def admin_panel(self):
        if not self.logged_in_user or self.logged_in_user.role != "admin":
            print("Access denied.")
            return

        while True:
            print("\n--- Admin Panel ---")
            print("1. Add Menu Item")
            print("2. View Orders")
            print("3. Update Order Status")
            print("4. Exit")

            choice = input("Choose an option: ")

            if choice == "1":
                name = input("Enter menu item name: ").strip()
                if not name:
                    print("Name cannot be empty.")
                    continue
                try:
                    price = float(input("Enter menu item price: "))
                    self.add_menu_item(name, price)
                except ValueError:
                    print("Invalid price. Please enter a number.")

            elif choice == "2":
                self.view_orders()

            elif choice == "3":
                try:
                    order_number = int(input("Enter order number: ")) - 1
                except ValueError:
                    print("Invalid order number.")
                    continue
                if order_number < 0 or order_number >= len(self.orders):
                    print("Invalid order number.")
                    continue
                status = input("Enter new status: ").strip()
                if status:
                    self.orders[order_number]["status"] = status
                    print("Status updated.")
                else:
                    print("Status cannot be empty.")

            elif choice == "4":
                break
            else:
                print("Invalid option.")

def get_choice(prompt: str = "Choose an option: ") -> str:
    return input(prompt).strip()

def main():
    restaurant = Restaurant()

    restaurant.add_menu_item("Burger", 10.99)
    restaurant.add_menu_item("Fries", 4.99)
    restaurant.add_menu_item("Soda", 2.99)

    restaurant.register_user("admin", "password", "admin")
    restaurant.register_user("user", "password", "user")

    while True:
        if not restaurant.logged_in_user:
            print("\n1. Login")
            print("2. Register")
            print("3. Exit")
            choice = get_choice()

            if choice == "1":
                username = input("Enter username: ").strip()
                password = input("Enter password: ")
                restaurant.login_user(username, password)
            elif choice == "2":
                username = input("Enter username: ").strip()
                password = input("Enter password: ")
                role = input("Enter role (admin/user): ")
                restaurant.register_user(username, password, role)
            elif choice == "3":
                break
            else:
                print("Invalid option.")
        else:
            is_admin = restaurant.logged_in_user.role == "admin"
            print(f"\nLogged in as {restaurant.logged_in_user.username} ({restaurant.logged_in_user.role})")
            print("1. Display Menu")
            print("2. Add to Cart")
            print("3. View Cart")
            print("4. Place Order")
            print("5. View Orders")
            if is_admin:
                print("6. Admin Panel")
                print("7. Logout")
            else:
                print("6. Logout")

            choice = get_choice()

            if choice == "1":
                restaurant.display_menu()
            elif choice == "2":
                restaurant.display_menu()
                if restaurant.menu:
                    item_number = input("Enter item number to add to cart: ")
                    restaurant.add_to_cart(item_number)
            elif choice == "3":
                restaurant.view_cart()
            elif choice == "4":
                restaurant.place_order()
            elif choice == "5":
                restaurant.view_orders()
            elif choice == "6" and is_admin:
                restaurant.admin_panel()
            elif (choice == "7" and is_admin) or (choice == "6" and not is_admin):
                restaurant.logout()
            else:
                print("Invalid option.")

if __name__ == "__main__":
    main()