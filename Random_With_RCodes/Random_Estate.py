import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class RealEstateApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Real Estate App")
        self.root.geometry("800x600")

        # Create database connection
        self.conn = sqlite3.connect("real_estate.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY,
                location TEXT,
                price REAL,
                size REAL,
                bedrooms INTEGER,
                bathrooms INTEGER
            )
        """)
        self.conn.commit()

        # Create tabs
        self.tab_control = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text="Add Property")
        self.tab_control.add(self.tab2, text="View Properties")
        self.tab_control.add(self.tab3, text="Delete Property")
        self.tab_control.pack(expand=1, fill="both")

        # Add property tab
        self.add_property_widgets()

        # View properties tab
        self.view_properties_widgets()

        # Delete property tab
        self.delete_property_widgets()

    def add_property_widgets(self):
        # Location
        tk.Label(self.tab1, text="Location:").grid(row=0, column=0, padx=5, pady=5)
        self.location_entry = tk.Entry(self.tab1, width=50)
        self.location_entry.grid(row=0, column=1, padx=5, pady=5)

        # Price
        tk.Label(self.tab1, text="Price:").grid(row=1, column=0, padx=5, pady=5)
        self.price_entry = tk.Entry(self.tab1, width=50)
        self.price_entry.grid(row=1, column=1, padx=5, pady=5)

        # Size
        tk.Label(self.tab1, text="Size (sqft):").grid(row=2, column=0, padx=5, pady=5)
        self.size_entry = tk.Entry(self.tab1, width=50)
        self.size_entry.grid(row=2, column=1, padx=5, pady=5)

        # Bedrooms
        tk.Label(self.tab1, text="Bedrooms:").grid(row=3, column=0, padx=5, pady=5)
        self.bedrooms_entry = tk.Entry(self.tab1, width=50)
        self.bedrooms_entry.grid(row=3, column=1, padx=5, pady=5)

        # Bathrooms
        tk.Label(self.tab1, text="Bathrooms:").grid(row=4, column=0, padx=5, pady=5)
        self.bathrooms_entry = tk.Entry(self.tab1, width=50)
        self.bathrooms_entry.grid(row=4, column=1, padx=5, pady=5)

        # Add property button
        self.add_property_button = tk.Button(self.tab1, text="Add Property", command=self.add_property)
        self.add_property_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def view_properties_widgets(self):
        # Properties text box
        self.properties_text = tk.Text(self.tab2, width=80, height=20)
        self.properties_text.pack(padx=5, pady=5)

        # View properties button
        self.view_properties_button = tk.Button(self.tab2, text="View Properties", command=self.view_properties)
        self.view_properties_button.pack(padx=5, pady=5)

    def delete_property_widgets(self):
        # Property ID
        tk.Label(self.tab3, text="Property ID:").grid(row=0, column=0, padx=5, pady=5)
        self.property_id_entry = tk.Entry(self.tab3, width=50)
        self.property_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Delete property button
        self.delete_property_button = tk.Button(self.tab3, text="Delete Property", command=self.delete_property)
        self.delete_property_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def add_property(self):
        location = self.location_entry.get()
        price = self.price_entry.get()
        size = self.size_entry.get()
        bedrooms = self.bedrooms_entry.get()
        bathrooms = self.bathrooms_entry.get()

        if location and price and size and bedrooms and bathrooms:
            try:
                self.cursor.execute("""
                    INSERT INTO properties (location, price, size, bedrooms, bathrooms)
                    VALUES (?, ?, ?, ?, ?)
                """, (location, float(price), float(size), int(bedrooms), int(bathrooms)))
                self.conn.commit()
                messagebox.showinfo("Success", "Property added successfully!")
                self.location_entry.delete(0, tk.END)
                self.price_entry.delete(0, tk.END)
                self.size_entry.delete(0, tk.END)
                self.bedrooms_entry.delete(0, tk.END)
                self.bathrooms_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Invalid input!")
        else:
            messagebox.showerror("Error", "Please fill out all fields!")

    def view_properties(self):
        self.properties_text.delete(1.0, tk.END)
        self.cursor.execute("SELECT * FROM properties")
        properties = self.cursor.fetchall()
        for property in properties:
            self.properties_text.insert(tk.END, f"ID: {property[0]}\nLocation: {property[1]}\nPrice: {property[2]}\nSize: {property[3]} sqft\nBedrooms: {property[4]}\nBathrooms: {property[5]}\n\n")

    def delete_property(self):
        property_id = self.property_id_entry.get()
        if property_id:
            try:
                self.cursor.execute("DELETE FROM properties WHERE id = ?", (int(property_id),))
                self.conn.commit()
                messagebox.showinfo("Success", "Property deleted successfully!")
                self.property_id_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Invalid property ID!")
        else:
            messagebox.showerror("Error", "Please enter a property ID!")

if __name__ == "__main__":
    root = tk.Tk()
    app = RealEstateApp(root)
    root.mainloop()