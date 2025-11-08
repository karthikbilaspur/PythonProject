import tkinter as tk
from tkinter import messagebox, ttk

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
        self.products = {}

        # Create the login page
        self.login_page()

    def login_page(self):
        self.clear_page()
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack()

        tk.Label(self.login_frame, text="Username:").pack()
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()

        tk.Label(self.login_frame, text="Password:").pack()
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack()

        tk.Button(self.login_frame, text="Login", command=self.login).pack()

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
        self.clear_page()
        self.admin_frame = tk.Frame(self.root)
        self.admin_frame.pack()

        tk.Button(self.admin_frame, text="Add Product", command=self.add_product_page).pack()
        tk.Button(self.admin_frame, text="Track Inventory", command=self.track_inventory_page).pack()
        tk.Button(self.admin_frame, text="Check Sales", command=self.check_sales_page).pack()
        tk.Button(self.admin_frame, text="Add User", command=self.add_user_page).pack()
        tk.Button(self.admin_frame, text="Remove User", command=self.remove_user_page).pack()
        tk.Button(self.admin_frame, text="Logout", command=self.login_page).pack()

    def user_dashboard(self):
        self.clear_page()
        self.user_frame = tk.Frame(self.root)
        self.user_frame.pack()

        tk.Button(self.user_frame, text="Make Invoice", command=self.make_invoice_page).pack()
        tk.Button(self.user_frame, text="Check Products", command=self.check_products_page).pack()
        tk.Button(self.user_frame, text="Logout", command=self.login_page).pack()

    def add_product_page(self):
        self.clear_page()
        self.add_product_frame = tk.Frame(self.root)
        self.add_product_frame.pack()

        tk.Label(self.add_product_frame, text="Product Name:").pack()
        self.product_name_entry = tk.Entry(self.add_product_frame)
        self.product_name_entry.pack()

        tk.Label(self.add_product_frame, text="Product Price:").pack()
        self.product_price_entry = tk.Entry(self.add_product_frame)
        self.product_price_entry.pack()

        tk.Label(self.add_product_frame, text="Product Quantity:").pack()
        self.product_quantity_entry = tk.Entry(self.add_product_frame)
        self.product_quantity_entry.pack()

        tk.Button(self.add_product_frame, text="Add Product", command=self.add_product_submit).pack()
        tk.Button(self.add_product_frame, text="Back", command=self.admin_dashboard).pack()

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
                    self.products[product_name] = {'price': product_price, 'quantity': product_quantity}
                    messagebox.showinfo("Product Added", f"Product '{product_name}' added successfully")
                    self.admin_dashboard()
            except ValueError:
                messagebox.showerror("Invalid Input", "Price and quantity must be numbers")
        else:
            messagebox.showerror("Invalid Input", "Please fill in all fields")

    def track_inventory_page(self):
        self.clear_page()
        self.track_inventory_frame = tk.Frame(self.root)
        self.track_inventory_frame.pack()

        if self.products:
            for product, details in self.products.items():
                tk.Label(self.track_inventory_frame, text=f"Product: {product}").pack()
                tk.Label(self.track_inventory_frame, text=f"Price: {details['price']}").pack()
                tk.Label(self.track_inventory_frame, text=f"Quantity: {details['quantity']}").pack()
                tk.Label(self.track_inventory_frame, text="").pack()
        else:
            tk.Label(self.track_inventory_frame, text="No products have been added yet").pack()

        tk.Button(self.track_inventory_frame, text="Back", command=self.admin_dashboard).pack()

    def check_sales_page(self):
        self.clear_page()
        self.check_sales_frame = tk.Frame(self.root)
        self.check_sales_frame.pack()

        tk.Label(self.check_sales_frame, text="Check Sales Page").pack()
        tk.Button(self.check_sales_frame, text="Back", command=self.admin_dashboard).pack()

    def add_user_page(self):
        self.clear_page()
        self.add_user_frame = tk.Frame(self.root)
        self.add_user_frame.pack()

        tk.Label(self.add_user_frame, text="Username:").pack()
        username_entry = tk.Entry(self.add_user_frame)
        username_entry.pack()
        tk.Label(self.add_user_frame, text="Password:").pack()
        password_entry = tk.Entry(self.add_user_frame, show="*")
        password_entry.pack()

        def submit_user():
            username = username_entry.get()
            password = password_entry.get()
            if username and password:
                self.credentials[username] = password
                messagebox.showinfo("User Added", f"User '{username}' added successfully")
                self.admin_dashboard()
            else:
                messagebox.showerror("Invalid Input", "Please fill in all fields")

        tk.Button(self.add_user_frame, text="Add User", command=submit_user).pack()
        tk.Button(self.add_user_frame, text="Back", command=self.admin_dashboard).pack()

    def remove_user_page(self):
        self.clear_page()
        self.remove_user_frame = tk.Frame(self.root)
        self.remove_user_frame.pack()

        tk.Label(self.remove_user_frame, text="Username:").pack()
        username_entry = tk.Entry(self.remove_user_frame)
        username_entry.pack()

        def submit_remove_user():
            username = username_entry.get()
            if username in self.credentials:
                del self.credentials[username]
                messagebox.showinfo("User Removed", f"User '{username}' removed successfully")
                self.admin_dashboard()
            else:
                messagebox.showerror("User Not Found", f"User '{username}' not found")

        tk.Button(self.remove_user_frame, text="Remove User", command=submit_remove_user).pack()
        tk.Button(self.remove_user_frame, text="Back", command=self.admin_dashboard).pack()

    def make_invoice_page(self):
        self.clear_page()
        self.make_invoice_frame = tk.Frame(self.root)
        self.make_invoice_frame.pack()

        if self.products:
            tk.Label(self.make_invoice_frame, text="Product:").pack()
            product_var = tk.StringVar()
            product_menu = ttk.Combobox(self.make_invoice_frame, textvariable=product_var)
            product_menu['values'] = list(self.products.keys())
            product_menu.pack()
            tk.Label(self.make_invoice_frame, text="Quantity:").pack()
            quantity_entry = tk.Entry(self.make_invoice_frame)
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
                            messagebox.showinfo("Invoice Made", f"Invoice made for {quantity} {product}(s)")
                            self.user_dashboard()
                    except ValueError:
                        messagebox.showerror("Invalid Input", "Quantity must be a number")
                else:
                    messagebox.showerror("Invalid Input", "Please fill in all fields")

            tk.Button(self.make_invoice_frame, text="Make Invoice", command=submit_invoice).pack()
        else:
            tk.Label(self.make_invoice_frame, text="No products have been added yet").pack()

        tk.Button(self.make_invoice_frame, text="Back", command=self.user_dashboard).pack()

    def check_products_page(self):
        self.clear_page()
        self.check_products_frame = tk.Frame(self.root)
        self.check_products_frame.pack()

        if self.products:
            for product, details in self.products.items():
                tk.Label(self.check_products_frame, text=f"Product: {product}").pack()
                tk.Label(self.check_products_frame, text=f"Price: {details['price']}").pack()
                tk.Label(self.check_products_frame, text=f"Quantity: {details['quantity']}").pack()
                tk.Label(self.check_products_frame, text="").pack()
        else:
            tk.Label(self.check_products_frame, text="No products have been added yet").pack()

        tk.Button(self.check_products_frame, text="Back", command=self.user_dashboard).pack()

    def clear_page(self):
        for widget in self.root.wacksliders():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesAndInventoryManagementSystem(root)
    root.mainloop()