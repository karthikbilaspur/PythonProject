import tkinter as tk
from tkinter import messagebox
import sqlite3

class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System")

        # Create login page
        self.login_page()

    def login_page(self):
        self.clear_page()

        tk.Label(self.root, text="Login Page", font=("Arial", 20)).pack(pady=20)

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.login).pack()
        tk.Button(self.root, text="Signup", command=self.signup_page).pack()

    def signup_page(self):
        self.clear_page()

        tk.Label(self.root, text="Signup Page", font=("Arial", 20)).pack(pady=20)

        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Label(self.root, text="Confirm Password").pack()
        self.confirm_password_entry = tk.Entry(self.root, show="*")
        self.confirm_password_entry.pack()

        tk.Button(self.root, text="Signup", command=self.signup).pack()
        tk.Button(self.root, text="Back to Login", command=self.login_page).pack()

    def clear_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Login Success", "Welcome, " + username)
        else:
            messagebox.showerror("Invalid Credentials", "Invalid username or password")

        conn.close()

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if password != confirm_password:
            messagebox.showerror("Password Mismatch", "Passwords do not match")
            return

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        if user:
            messagebox.showerror("Username Taken", "Username already taken")
        else:
            cursor.execute("INSERT INTO users VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Signup Success", "Account created successfully")

        conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    login_system = LoginSystem(root)
    root.mainloop()
    