import tkinter as tk
from tkinter import messagebox
import string
import secrets

class PasswordGenerator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Password Generator")

        # Password length
        tk.Label(self.window, text="Password Length:").grid(row=0, column=0)
        self.length_entry = tk.Entry(self.window)
        self.length_entry.insert(0, "12")
        self.length_entry.grid(row=0, column=1)

        # Character options
        tk.Label(self.window, text="Character Options:").grid(row=1, column=0)
        self.uppercase_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self.window, text="Uppercase Letters", variable=self.uppercase_var).grid(row=2, column=0)
        self.numbers_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self.window, text="Numbers", variable=self.numbers_var).grid(row=2, column=1)
        self.special_chars_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self.window, text="Special Characters", variable=self.special_chars_var).grid(row=2, column=2)

        # Generate password button
        tk.Button(self.window, text="Generate Password", command=self.generate_password).grid(row=3, column=0, columnspan=3)

        # Password output
        tk.Label(self.window, text="Generated Password:").grid(row=4, column=0)
        self.password_label = tk.Label(self.window, text="")
        self.password_label.grid(row=4, column=1, columnspan=2)

    def generate_password(self):
        try:
            length = int(self.length_entry.get())
            if length < 8:
                messagebox.showerror("Error", "Password length should be at least 8 characters")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid password length")
            return

        characters = string.ascii_lowercase
        if self.uppercase_var.get():
            characters += string.ascii_uppercase
        if self.numbers_var.get():
            characters += string.digits
        if self.special_chars_var.get():
            characters += string.punctuation

        password = ''.join(secrets.choice(characters) for _ in range(length))
        self.password_label.config(text=password)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    generator = PasswordGenerator()
    generator.run()