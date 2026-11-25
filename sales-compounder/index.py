import hashlib
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from collections.abc import Callable, Sequence

DB = "sales_inventory.db"

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

class DBLayer:
    def __init__(self, path: str = DB):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password_hash TEXT NOT NULL, role TEXT NOT NULL)")
        self.conn.execute("CREATE TABLE IF NOT EXISTS products(name TEXT PRIMARY KEY, price REAL NOT NULL CHECK(price>0), quantity INTEGER NOT NULL CHECK(quantity>=0))")
        self.conn.execute("CREATE TABLE IF NOT EXISTS sales(id INTEGER PRIMARY KEY AUTOINCREMENT, product TEXT NOT NULL, quantity INTEGER NOT NULL, unit_price REAL NOT NULL, total REAL NOT NULL, sold_by TEXT, sold_at TEXT)")
        self.conn.commit()
        for u, p, r in [("ADMIN", "ADMIN", "ADMIN"), ("USER", "USER", "USER")]:
            if not self.get_user(u):
                self.add_user(u, p, r)
    def get_user(self, username: str):
        return self.conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    def add_user(self, username: str, password: str, role: str = "USER") -> bool:
        try:
            self.conn.execute("INSERT INTO users VALUES (?,?,?)", (username, hash_pw(password), role))
            self.conn.commit(); return True
        except sqlite3.IntegrityError:
            return False
    def remove_user(self, username: str):
        self.conn.execute("DELETE FROM users WHERE username=?", (username,)); self.conn.commit()
    def list_users(self):
        return self.conn.execute("SELECT username, role FROM users ORDER BY username").fetchall()
    def count_admins(self):
        return self.conn.execute("SELECT COUNT(*) c FROM users WHERE role='ADMIN'").fetchone()["c"]
    def list_products(self):
        return self.conn.execute("SELECT * FROM products ORDER BY name").fetchall()
    def get_product(self, name: str):
        return self.conn.execute("SELECT * FROM products WHERE name=?", (name,)).fetchone()
    def upsert_product(self, name: str, price: float, qty: int):
        # Adds new, or if exists: updates price and ADDS quantity
        cur = self.get_product(name)
        if cur:
            self.conn.execute("UPDATE products SET price=?, quantity=quantity+? WHERE name=?", (price, qty, name))
        else:
            self.conn.execute("INSERT INTO products VALUES (?,?,?)", (name, price, qty))
        self.conn.commit()
    def set_product_qty(self, name: str, qty: int):
        self.conn.execute("UPDATE products SET quantity=? WHERE name=?", (qty, name)); self.conn.commit()
    def delete_product(self, name: str):
        self.conn.execute("DELETE FROM products WHERE name=?", (name,)); self.conn.commit()
    def record_sale(self, product: str, qty: int, unit_price: float, sold_by: str) -> float:
        total = qty * unit_price
        self.conn.execute("INSERT INTO sales(product,quantity,unit_price,total,sold_by,sold_at) VALUES (?,?,?,?,?,?)",
                          (product, qty, unit_price, total, sold_by, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.execute("UPDATE products SET quantity=quantity-? WHERE name=?", (qty, product))
        self.conn.commit()
        return total
    def list_sales(self):
        return self.conn.execute("SELECT * FROM sales ORDER BY id DESC").fetchall()
    def sales_total(self):
        r = self.conn.execute("SELECT COALESCE(SUM(total),0) t, COALESCE(SUM(quantity),0) q FROM sales").fetchone()
        return r["t"], r["q"]

class App:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.title("Sales and Inventory Management System")
        self.root.geometry("700x520")
        self.db = DBLayer()
        self.current_user = None
        self.current_role = None
        self.login_page()

    # --- navigation ---
    def clear_page(self):
        # FIXED: was root.wacksliders() which crashes
        for w in self.root.winfo_children():
            w.destroy()
    def back_to_dashboard(self):
        if self.current_role == "ADMIN":
            self.admin_dashboard()
        else:
            self.user_dashboard()
    def logout(self):
        self.current_user = None; self.current_role = None
        self.login_page()

    # --- login ---
    def login_page(self):
        self.clear_page()
        f = tk.Frame(self.root, padx=20, pady=20); f.pack(expand=True)
        tk.Label(f, text="Sales and Inventory", font=("Arial", 16, "bold")).pack(pady=(0, 10))
        tk.Label(f, text="Username:").pack(anchor="w")
        self.username_entry = tk.Entry(f, width=35); self.username_entry.pack(pady=(0, 8))
        tk.Label(f, text="Password:").pack(anchor="w")
        self.password_entry = tk.Entry(f, width=35, show="*"); self.password_entry.pack(pady=(0, 12))
        self.password_entry.bind("<Return>", lambda _event: self.login())
        tk.Button(f, text="Login", width=20, command=self.login).pack()
        tk.Label(f, text="Default: ADMIN / ADMIN  •  USER / USER", fg="grey").pack(pady=10)
    def login(self):
        u = self.username_entry.get().strip(); p = self.password_entry.get()
        row = self.db.get_user(u)
        if row and row["password_hash"] == hash_pw(p):
            self.current_user = u; self.current_role = row["role"]
            self.back_to_dashboard()
        else:
            messagebox.showerror("Invalid Credentials", "Invalid username or password")

    # --- dashboards ---
    def admin_dashboard(self):
        self.clear_page()
        f = tk.Frame(self.root, padx=20, pady=20); f.pack()
        tk.Label(f, text=f"Admin Dashboard — {self.current_user}", font=("Arial", 14, "bold")).pack(pady=(0, 12))
        for txt, cmd in [("Add / Restock Product", self.add_product_page),
                         ("Track Inventory", self.track_inventory_page),
                         ("Check Sales", self.check_sales_page),
                         ("Manage Users", self.manage_users_page),
                         ("Logout", self.logout)]:
            tk.Button(f, text=txt, width=30, command=cmd).pack(pady=3)
    def user_dashboard(self):
        self.clear_page()
        f = tk.Frame(self.root, padx=20, pady=20); f.pack()
        tk.Label(f, text=f"Cashier Dashboard — {self.current_user}", font=("Arial", 14, "bold")).pack(pady=(0, 12))
        for txt, cmd in [("Make Invoice (Sell)", self.make_invoice_page),
                         ("Check Products", self.check_products_page),
                         ("Logout", self.logout)]:
            tk.Button(f, text=txt, width=30, command=cmd).pack(pady=3)

    # --- helpers for tables ---
    def table(self, parent: tk.Misc, columns: list[str], rows: Sequence[Sequence[object]]) -> ttk.Treeview:
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=12)
        for c in columns:
            tree.heading(c, text=c); tree.column(c, width=140)
        for r in rows:
            tree.insert("", "end", values=tuple(r))
        def scroll(*args: str) -> None:
            tree.tk.call(tree, "yview", *args)

        sb = ttk.Scrollbar(parent, orient="vertical", command=scroll)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True); sb.pack(side="right", fill="y")
        return tree

    # --- products ---
    def add_product_page(self):
        self.clear_page()
        f = tk.Frame(self.root, padx=20, pady=20); f.pack()
        tk.Label(f, text="Add / Restock Product", font=("Arial", 13, "bold")).pack(pady=(0, 10))
        entries: dict[str, tk.Entry] = {}
        for label in ["Product Name:", "Product Price:", "Product Quantity (to add):"]:
            tk.Label(f, text=label).pack(anchor="w")
            e = tk.Entry(f, width=35); e.pack(pady=(0, 6)); entries[label] = e
        def submit():
            name = entries["Product Name:"].get().strip()
            try:
                price = float(entries["Product Price:"].get()); qty = int(entries["Product Quantity (to add):"].get())
            except ValueError:
                messagebox.showerror("Invalid Input", "Price and quantity must be numbers"); return
            if not name or price <= 0 or qty <= 0:
                messagebox.showerror("Invalid Input", "Fill all fields; price and quantity must be positive"); return
            self.db.upsert_product(name, price, qty)
            messagebox.showinfo("Saved", f"'{name}' saved (quantity added).")
            self.admin_dashboard()
        tk.Button(f, text="Save Product", command=submit).pack(pady=6)
        tk.Button(f, text="Back", command=self.admin_dashboard).pack()
    def track_inventory_page(self):
        self.clear_page()
        f = tk.Frame(self.root, padx=20, pady=15); f.pack(fill="both", expand=True)
        tk.Label(f, text="Inventory", font=("Arial", 13, "bold")).pack()
        rows = [(r["name"], f"{r['price']:.2f}", r["quantity"], "LOW" if r["quantity"] < 5 else "") for r in self.db.list_products()]
        if not rows:
            tk.Label(f, text="No products yet.").pack(pady=10)
        else:
            tf = tk.Frame(f); tf.pack(fill="both", expand=True, pady=8)
            tree = self.table(tf, ["Product", "Price", "Quantity", "Status"], rows)
            def delete_selected():
                sel = tree.selection()
                if not sel: return
                name = tree.item(sel[0])["values"][0]
                if messagebox.askyesno("Delete", f"Delete '{name}'?"):
                    self.db.delete_product(name); self.track_inventory_page()
            tk.Button(f, text="Delete Selected Product", command=delete_selected).pack(pady=4)
        tk.Button(f, text="Back", command=self.admin_dashboard).pack(pady=6)
    def check_products_page(self):
        self.clear_page()
        f = tk.Frame(self.root, padx=20, pady=15); f.pack(fill="both", expand=True)
        tk.Label(f, text="Products", font=("Arial", 13, "bold")).pack()
        rows = [(r["name"], f"{r['price']:.2f}", r["quantity"]) for r in self.db.list_products()]
        if not rows:
            tk.Label(f, text="No products have been added yet").pack(pady=10)
        else:
            tf = tk.Frame(f); tf.pack(fill="both", expand=True, pady=8); self.table(tf, ["Product", "Price", "Quantity"], rows)
        tk.Button(f, text="Back", command=self.back_to_dashboard).pack(pady=6)

    # --- sales / invoice ---
    def check_sales_page(self):
        self.clear_page()
        f = tk.Frame(self.root, padx=20, pady=15); f.pack(fill="both", expand=True)
        total, qty = self.db.sales_total()
        tk.Label(f, text="Check Sales", font=("Arial", 13, "bold")).pack()
        tk.Label(f, text=f"Total Revenue: ₹{total:.2f}  •  Units Sold: {qty}  •  Transactions: {len(self.db.list_sales())}").pack(pady=4)
        rows = [(r["id"], r["product"], r["quantity"], f"{r['unit_price']:.2f}", f"{r['total']:.2f}", r["sold_by"] or "", r["sold_at"]) for r in self.db.list_sales()]
        if rows:
            tf = tk.Frame(f); tf.pack(fill="both", expand=True, pady=8)
            self.table(tf, ["ID", "Product", "Qty", "Unit Price", "Total", "Sold By", "When"], rows)
        else:
            tk.Label(f, text="No sales yet.").pack()
        tk.Button(f, text="Back", command=self.admin_dashboard).pack(pady=6)
    def make_invoice_page(self):
        self.clear_page()
        f = tk.Frame(self.root, padx=20, pady=20); f.pack()
        tk.Label(f, text="Make Invoice", font=("Arial", 13, "bold")).pack(pady=(0, 10))
        products = self.db.list_products()
        if not products:
            tk.Label(f, text="No products have been added yet").pack()
            tk.Button(f, text="Back", command=self.user_dashboard).pack(pady=8); return
        tk.Label(f, text="Product:").pack(anchor="w")
        var = tk.StringVar(); combo = ttk.Combobox(f, textvariable=var, values=[r["name"] for r in products], state="readonly", width=32); combo.pack(pady=(0, 6))
        tk.Label(f, text="Quantity:").pack(anchor="w")
        qty_entry = tk.Entry(f, width=35); qty_entry.pack(pady=(0, 6))
        total_label = tk.Label(f, text=""); total_label.pack()
        def preview(_event: tk.Event[tk.Misc]) -> None:
            r = self.db.get_product(var.get())
            if r: total_label.config(text=f"Price: ₹{r['price']:.2f}  •  In stock: {r['quantity']}")
        combo.bind("<<ComboboxSelected>>", preview)
        def submit():
            name = var.get()
            if not name: messagebox.showerror("Invalid Input", "Select a product"); return
            try: qty = int(qty_entry.get())
            except ValueError: messagebox.showerror("Invalid Input", "Quantity must be a number"); return
            r = self.db.get_product(name)
            if qty <= 0: messagebox.showerror("Invalid Input", "Quantity must be positive"); return
            if qty > r["quantity"]: messagebox.showerror("Invalid Input", "Not enough quantity in stock"); return
            sold_by = self.current_user
            if sold_by is None:
                return
            total = self.db.record_sale(name, qty, r["price"], sold_by)  # FIXED: deducts stock + records sale
            messagebox.showinfo("Invoice Made", f"Invoice: {qty} × {name} @ ₹{r['price']:.2f} = ₹{total:.2f}\nStock left: {r['quantity'] - qty}")
            self.user_dashboard()
        tk.Button(f, text="Make Invoice", command=submit).pack(pady=6)
        tk.Button(f, text="Back", command=self.user_dashboard).pack()

    # --- users ---
    def manage_users_page(self):
        self.clear_page()
        f = tk.Frame(self.root, padx=20, pady=15); f.pack(fill="both", expand=True)
        tk.Label(f, text="Manage Users", font=("Arial", 13, "bold")).pack()
        rows = [(r["username"], r["role"]) for r in self.db.list_users()]
        tf = tk.Frame(f); tf.pack(fill="both", expand=True, pady=8)
        tree = self.table(tf, ["Username", "Role"], rows)
        # Add user form
        af = tk.Frame(f); af.pack(pady=6)
        tk.Label(af, text="New Username:").grid(row=0, column=0); ue = tk.Entry(af); ue.grid(row=0, column=1, padx=4)
        tk.Label(af, text="Password:").grid(row=1, column=0); pe = tk.Entry(af, show="*"); pe.grid(row=1, column=1, padx=4)
        tk.Label(af, text="Role:").grid(row=2, column=0); role_var = tk.StringVar(value="USER")
        ttk.Combobox(af, textvariable=role_var, values=["USER", "ADMIN"], state="readonly", width=18).grid(row=2, column=1, padx=4)
        def add():
            u, p = ue.get().strip(), pe.get()
            if not u or not p: messagebox.showerror("Invalid Input", "Fill in all fields"); return
            if self.db.add_user(u, p, role_var.get()):
                messagebox.showinfo("User Added", f"User '{u}' added"); self.manage_users_page()
            else: messagebox.showerror("Exists", f"User '{u}' already exists")
        def remove():
            sel = tree.selection()
            if not sel: messagebox.showerror("Select", "Select a user to remove"); return
            u = tree.item(sel[0])["values"][0]
            if u == self.current_user: messagebox.showerror("Blocked", "Cannot remove yourself while logged in"); return
            if self.db.get_user(u)["role"] == "ADMIN" and self.db.count_admins() <= 1:
                messagebox.showerror("Blocked", "Cannot remove the last admin"); return
            if messagebox.askyesno("Remove", f"Remove user '{u}'?"):
                self.db.remove_user(u); self.manage_users_page()
        tk.Button(af, text="Add User", command=add).grid(row=3, column=0, columnspan=2, pady=6)
        tk.Button(f, text="Remove Selected User", command=remove).pack(pady=2)
        tk.Button(f, text="Back", command=self.admin_dashboard).pack(pady=4)

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()