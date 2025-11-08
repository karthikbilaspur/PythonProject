import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
# Define the main application class
class SalesAndInventoryManagementSystem:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Sales and Inventory Management System")

        # Define the login credentials
        self.credentials = {
            "ADMIN": "ADMIN",
            "USER": "USER"
        }

        # Define the current user
        self.current_user = None

        # Create the login frame
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack()

        # Create the login form
        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.credentials and self.credentials[username] == password:
            self.current_user = username
            self.login_frame.pack_forget()
            if username == "ADMIN":
                self.admin_dashboard()
            else:
                self.user_dashboard()
        else:
            messagebox.showerror("Invalid Credentials", "Invalid username or password")

    def admin_dashboard(self):
        # Create the admin dashboard frame
        self.admin_frame = tk.Frame(self.root)
        self.admin_frame.pack()

        # Create the admin dashboard buttons
        self.add_product_button = tk.Button(self.admin_frame, text="Add Product", command=self.add_product)
        self.add_product_button.pack()

        self.track_inventory_button = tk.Button(self.admin_frame, text="Track Inventory", command=self.track_inventory)
        self.track_inventory_button.pack()

        self.check_sales_button = tk.Button(self.admin_frame, text="Check Sales", command=self.check_sales)
        self.check_sales_button.pack()

        self.add_user_button = tk.Button(self.admin_frame, text="Add User", command=self.add_user)
        self.add_user_button.pack()

        self.remove_user_button = tk.Button(self.admin_frame, text="Remove User", command=self.remove_user)
        self.remove_user_button.pack()

    def user_dashboard(self):
        # Create the user dashboard frame
        self.user_frame = tk.Frame(self.root)
        self.user_frame.pack()

        # Create the user dashboard buttons
        self.make_invoice_button = tk.Button(self.user_frame, text="Make Invoice", command=self.make_invoice)
        self.make_invoice_button.pack()

        self.check_products_button = tk.Button(self.user_frame, text="Check Products", command=self.check_products)
        self.check_products_button.pack()

    def add_product(self):
        # Create the add product frame
        self.add_product_frame = tk.Frame(self.root)
        self.add_product_frame.pack()

        # Create the add product form
        self.product_name_label = tk.Label(self.add_product_frame, text="Product Name:")
        self.product_name_label.pack()
        self.product_name_entry = tk.Entry(self.add_product_frame)
        self.product_name_entry.pack()

        self.product_price_label = tk.Label(self.add_product_frame, text="Product Price:")
        self.product_price_label.pack()
        self.product_price_entry = tk.Entry(self.add_product_frame)
        self.product_price_entry.pack()

        self.product_quantity_label = tk.Label(self.add_product_frame, text="Product Quantity:")
        self.product_quantity_label.pack()
        self.product_quantity_entry = tk.Entry(self.add_product_frame)
        self.product_quantity_entry.pack()

        self.add_product_submit_button = tk.Button(self.add_product_frame, text="Add Product", command=self.add_product_submit)
        self.add_product_submit_button.pack()

def add_product_submit(self):
    product_name = self.product_name_entry.get()
    product_price = self.product_price_entry.get()
    product_quantity = self.product_quantity_entry.get()

    if product_name and product_price and product_quantity:
        try:
            product_price = float(product_price)
            product_quantity = int(product_quantity)
            if product_price <= 0 or product_quantity <= 0:
                messagebox.showerror("Invalid Input", "Price and quantity must be positive numbers")
            else:
                # Add product to database or data structure
                # For simplicity, let's use a dictionary
                if not hasattr(self, 'products'):
                    self.products = {}
                self.products[product_name] = {'price': product_price, 'quantity': product_quantity}
                messagebox.showinfo("Product Added", f"Product '{product_name}' added successfully")
                self.add_product_frame.pack_forget()
        except ValueError:
            messagebox.showerror("Invalid Input", "Price and quantity must be numbers")
    else:
        messagebox.showerror("Invalid Input", "Please fill in all fields")

    def track_inventory(self):
    if hasattr(self, 'products'):
        inventory_window = tk.Toplevel(self.root)
        inventory_window.title("Inventory")
        inventory_text = tk.Text(inventory_window)
        inventory_text.pack()
        for product, details in self.products.items():
            inventory_text.insert(tk.END, f"Product: {product}\nPrice: {details['price']}\nQuantity: {details['quantity']}\n\n")
    else:
        messagebox.showinfo("No Products", "No products have been added yet")

    def add_user(self):
    add_user_window = tk.Toplevel(self.root)
    add_user_window.title("Add User")
    tk.Label(add_user_window, text="Username:").pack()
    username_entry = tk.Entry(add_user_window)
    username_entry.pack()
    tk.Label(add_user_window, text="Password:").pack()
    password_entry = tk.Entry(add_user_window, show="*")
    password_entry.pack()
    def submit_user():
        username = username_entry.get()
        password = password_entry.get()
        if username and password:
            # Add user to database or data structure
            # For simplicity, let's use a dictionary
            if not hasattr(self, 'users'):
                self.users = {}
            self.users[username] = password
            messagebox.showinfo("User Added", f"User '{username}' added successfully")
            add_user_window.destroy()
        else:
            messagebox.showerror("Invalid Input", "Please fill in all fields")
    tk.Button(add_user_window, text="Add User", command=submit_user).pack()

    def remove_user(self):
    if hasattr(self, 'users'):
        remove_user_window = tk.Toplevel(self.root)
        remove_user_window.title("Remove User")
        tk.Label(remove_user_window, text="Username:").pack()
        username_entry = tk.Entry(remove_user_window)
        username_entry.pack()
        def submit_remove_user():
            username = username_entry.get()
            if username in self.users:
                del self.users[username]
                messagebox.showinfo("User Removed", f"User '{username}' removed successfully")
                remove_user_window.destroy()
            else:
                messagebox.showerror("User Not Found", f"User '{username}' not found")
        tk.Button(remove_user_window, text="Remove User", command=submit_remove_user).pack()
    else:
        messagebox.showinfo("No Users", "No users have been added yet")

    def make_invoice(self):
    if hasattr(self, 'products'):
        make_invoice_window = tk.Toplevel(self.root)
        make_invoice_window.title("Make Invoice")
        tk.Label(make_invoice_window, text="Product:").pack()
        product_var = tk.StringVar()
        product_menu = ttk.Combobox(make_invoice_window, textvariable=product_var)
        product_menu['values'] = list(self.products.keys())
        product_menu.pack()
        tk.Label(make_invoice_window, text="Quantity:").pack()
        quantity_entry = tk.Entry(make_invoice_window)
        quantity_entry.pack()
        def submit_invoice():
            product = product_var.get()
            quantity = quantity_entry.get()
            if product and quantity:
                try:
                    quantity = int(quantity)
                    if quantity <= 0:
                        messagebox.showerror("Invalid Input", "Quantity must be a positive number")
                    elif quantity > self.products[product]['quantity']:
                        messagebox.showerror("Invalid Input", "Not enough quantity in stock")
                    else:
                        # Make invoice logic here
                        # For simplicity, let's just show a message
                        messagebox.showinfo("Invoice Made", f"Invoice made for {quantity} {product}(s)")
                        make_invoice_window.destroy()
                except ValueError:
                    messagebox.showerror("Invalid Input", "Quantity must be a number")
            else:
                messagebox.showerror("Invalid Input", "Please fill in all fields")
        tk.Button(make_invoice_window, text="Make Invoice", command=submit_invoice).pack()
    else:
        messagebox.showinfo("No Products", "No products have been added yet")    

def check_products(self):
    if hasattr(self, 'products'):
        check_products_window = tk.Toplevel(self.root)
        check_products_window.title("Check Products")

        # Create a frame to hold the product list
        product_frame = tk.Frame(check_products_window)
        product_frame.pack(fill="both", expand=True)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(product_frame)
        scrollbar.pack(side="right", fill="y")

        # Create a text box to display the products
        check_products_text = tk.Text(product_frame, yscrollcommand=scrollbar.set)
        check_products_text.pack(side="left", fill="both", expand=True)

        # Configure the scrollbar
        scrollbar.config(command=check_products_text.yview)

        # Insert products into the text box
        for product, details in self.products.items():
            check_products_text.insert(tk.END, f"Product: {product}\nPrice: {details['price']}\nQuantity: {details['quantity']}\n\n")

        # Make the text box read-only
        check_products_text.config(state="disabled")
    else:
        messagebox.showinfo("No Products", "No products have been added yet")

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesAndInventoryManagementSystem(root)
    root.mainloop()