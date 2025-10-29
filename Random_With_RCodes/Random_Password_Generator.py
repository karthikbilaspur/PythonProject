import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip

class PasswordGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Random Password Generator")

        self.length = tk.IntVar()
        self.strength = tk.IntVar()

        self.create_widgets()

    def create_widgets(self):
        # Create frames
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP)

        length_frame = tk.Frame(self.root)
        length_frame.pack(side=tk.TOP)

        strength_frame = tk.Frame(self.root)
        strength_frame.pack(side=tk.LEFT)

        output_frame = tk.Frame(self.root)
        output_frame.pack(side=tk.RIGHT)

        # Create widgets
        tk.Label(top_frame, text="Random Password Generator", font=("Lucida Console", 20, "italic")).pack()

        tk.Label(length_frame, text="Length of Password").pack(side=tk.LEFT)
        tk.Scale(length_frame, from_=6, to=24, orient=tk.HORIZONTAL, variable=self.length).pack(side=tk.LEFT)

        tk.Label(strength_frame, text="Strength").pack()
        tk.Radiobutton(strength_frame, text="Low", variable=self.strength, value=1).pack()
        tk.Radiobutton(strength_frame, text="Medium", variable=self.strength, value=2).pack()
        tk.Radiobutton(strength_frame, text="High", variable=self.strength, value=3).pack()

        tk.Button(output_frame, text="Generate Password", command=self.generate_password).pack()
        self.password_entry = tk.Entry(output_frame, width=50)
        self.password_entry.pack()
        tk.Button(output_frame, text="Copy", command=self.copy_password).pack()

    def generate_password(self):
        length = self.length.get()
        strength = self.strength.get()

        if strength == 0:
            messagebox.showwarning("Warning", "Select a password strength")
            return

        characters = string.ascii_lowercase + string.digits
        if strength == 2:
            characters += string.ascii_uppercase
        elif strength == 3:
            characters += string.ascii_uppercase + string.punctuation

        password = ''.join(secrets.choice(characters) for _ in range(length))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def copy_password(self):
        password = self.password_entry.get()
        pyperclip.copy(password)
        messagebox.showinfo("Message", "Copied to clipboard!")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    generator = PasswordGenerator()
    generator.run()