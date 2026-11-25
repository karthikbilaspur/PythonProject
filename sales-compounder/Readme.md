# Sales and Inventory Management System

A desktop app built with Python, Tkinter, and SQLite for managing products, stock, sales/invoices, and users — with separate Admin and Cashier (USER) roles.

Features
Admin
Add / Restock Product — add a new product, or restock an existing one. Restocking updates the price and adds to the existing quantity.
Track Inventory — view all products with price, quantity, and a LOW flag when quantity < 5. Delete a selected product.
Check Sales — view total revenue, total units sold, transaction count, and full sales history (ID, product, qty, unit price, total, sold by, timestamp).
Manage Users — view all users, add a new USER/ADMIN, remove users (with protection against removing yourself or the last admin).
Cashier (USER)
Make Invoice (Sell) — pick a product, enter quantity, see live price + stock, and sell. Sale is recorded and stock is deducted automatically.
Check Products — view product list with price and quantity (read-only).
Auth & Security
Login with username + password.
Passwords stored as SHA-256 hashes (not plaintext).
Default accounts are seeded on first run (see below).
Sales record who sold them (sold_by) and when (sold_at).
Tech Stack
Layer Technology
UI Tkinter + ttk (Treeview, Combobox, Scrollbar)
Database SQLite (sqlite3, row_factory = sqlite3.Row)
Auth hashlib.sha256
Language Python 3
Project Structure
sales_inventory.py        # Main app (DBLayer + App) — the file you pasted
sales_inventory.db        # SQLite DB, auto-created on first run
README.md                 # This file
The code you shared has no filename in it. Save it as sales_inventory.py (or any .py name) — the DB file name is fixed inside the code as sales_inventory.db.

Setup & Run
Requirements
Python 3.9+ (uses list[str], dict[str, ...], collections.abc.Callable/Sequence type hints)
No third-party packages needed — only the standard library (tkinter, sqlite3, hashlib)
Run it
python sales_inventory.py
On first run it creates sales_inventory.db with 3 tables (users, products, sales) and seeds the default accounts.

Default Logins
Username Password Role
ADMIN ADMIN ADMIN
USER USER USER
Change these passwords after first login in a real deployment — see Limitations below. There is currently no change-password screen; you would need to delete/re-create the user in Manage Users, or update the DB directly.

How It Works
Database Schema
users(username TEXT PRIMARY KEY, password_hash TEXT NOT NULL, role TEXT NOT NULL)
products(name TEXT PRIMARY KEY, price REAL NOT NULL CHECK(price>0), quantity INTEGER NOT NULL CHECK(quantity>=0))
sales(id INTEGER PRIMARY KEY AUTOINCREMENT, product TEXT NOT NULL, quantity INTEGER NOT NULL,
      unit_price REAL NOT NULL, total REAL NOT NULL, sold_by TEXT, sold_at TEXT)
Key Flows
Login → DBLayer.get_user() → compare sha256(password) → open Admin or Cashier dashboard by role.
Add / Restock → upsert_product(name, price, qty) → INSERT if new, else UPDATE price + quantity = quantity + qty.
Sell → validate qty > 0 and qty <= stock → record_sale() inserts into sales and does quantity = quantity - qty in one commit.
Manage Users → add_user() / remove_user() with guards: cannot remove yourself, cannot remove the last ADMIN.
File / Class Overview
Component What it does
hash_pw(pw) Returns sha256 hex digest of a password
DBLayer All SQLite access: users, products, sales
App All Tkinter UI: login, dashboards, product/sales/user pages
App.table() Helper that builds a scrollable ttk.Treeview
App.clear_page() Destroys all widgets to switch screens
Usage Walkthrough
Log in as ADMIN / ADMIN.
Add / Restock Product → e.g. Notebook, price 50, quantity 20 → Save.
Add a cashier via Manage Users if needed.
Log out, log in as USER / USER.
Make Invoice → select Notebook, quantity 2 → Make Invoice. Stock drops to 18.
Log back in as Admin → Check Sales shows the ₹100.00 sale, Track Inventory shows updated stock.
Honest Review — Bugs / Drawbacks / Limitations
Short version: it works as a small college / demo project, but don't use it as-is for a real shop.

Weak default passwords + no password change: ADMIN/ADMIN and USER/USER are hardcoded and seeded on every fresh DB. Anyone who knows the defaults gets in.
SHA-256 without salt: hash_pw() is unsalted SHA-256. Identical passwords have identical hashes, and it's fast to brute-force. For real use, use bcrypt / argon2 / hashlib.pbkdf2_hmac with a per-user salt.
No concurrency / transaction safety on sales: record_sale() reads stock in the UI, then decrements it. Two cashiers selling the last item at the same time could oversell. No BEGIN IMMEDIATE / stock check inside the transaction.
No edit flows: You can't edit a product's price/name in place (only restock-overwrite price), can't edit a user/role, can't void/refund a sale, and can't change a password.
No search / filter / pagination: Product and sales tables list everything. They'll get unwieldy with many rows.
Sales keep product name as text, not a foreign key: If you delete a product, old sales still show its name (which is arguably good for history), but renaming a product breaks the link.
Single DB file, no backup/export: No CSV/PDF invoice export, no backup, no audit log beyond sales.
UI quirks: Fixed 700x520 window, tables use a fixed column width (140), no keyboard shortcuts beyond Enter on login, and deleting a product has no check for whether it has sales history.
Minor code notes: App.table() defines a custom scroll() wrapper instead of passing tree.yview directly; make_invoice_page guards sold_by is None after already checking stock, which is defensive but unreachable in normal flow since login sets it.
Possible Enhancements
Salted password hashing + change-password + force password change on first login
Edit product, void/refund sale, low-stock threshold setting
Search/filter products and sales by name/date
Printable/PDF invoice + CSV export
Atomic sale transaction with stock check inside the DB layer
Barcode / category / supplier fields
License
No license specified — treat as a personal / coursework project unless you add one.
