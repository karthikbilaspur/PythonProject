import tkinter as tk
from tkinter import messagebox
import random
import string

class PasswordGenerator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Password Generator")

        self.length_label = tk.Label(self.window, text="Password Length:")
        self.length_label.pack()
        self.length_entry = tk.Entry(self.window)
        self.length_entry.pack()

        self.complexity_label = tk.Label(self.window, text="Password Complexity:")
        self.complexity_label.pack()
        self.complexity = tk.StringVar()
        self.complexity.set("Simple")
        self.complexity_simple = tk.Radiobutton(self.window, text="Simple (a-z)", variable=self.complexity, value="Simple")
        self.complexity_simple.pack()
        self.complexity_medium = tk.Radiobutton(self.window, text="Medium (a-z, A-Z)", variable=self.complexity, value="Medium")
        self.complexity_medium.pack()
        self.complexity_complex = tk.Radiobutton(self.window, text="Complex (a-z, A-Z, 0-9, !@#$%^&*)", variable=self.complexity, value="Complex")
        self.complexity_complex.pack()

        self.generate_button = tk.Button(self.window, text="Generate Password", command=self.generate_password)
        self.generate_button.pack()

        self.password_label = tk.Label(self.window, text="Generated Password:")
        self.password_label.pack()
        self.password_entry = tk.Text(self.window, height=5, width=40)
        self.password_entry.pack()

    def generate_password(self):
        try:
            length = int(self.length_entry.get())
            complexity = self.complexity.get()

            if complexity == "Simple":
                characters = string.ascii_lowercase
            elif complexity == "Medium":
                characters = string.ascii_letters
            elif complexity == "Complex":
                characters = string.ascii_letters + string.digits + "!@#$%^&*"

            password = ''.join(random.choice(characters) for _ in range(length))
            self.password_entry.delete('1.0', tk.END)
            self.password_entry.insert(tk.END, password)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid password length")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    generator = PasswordGenerator()
    generator.run()