import requests
import tkinter as tk
from tkinter import messagebox

class QuoteGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Random Quote Generator")

        self.quote_label = tk.Label(self.root, text="", title="Click Get Quote", wraplength=400, font=("Arial", 14))
        self.quote_label.pack(padx=20, pady=20)

        self.author_label = tk.Label(self.root, text="", font=("Arial", 12, "italic"))
        self.author_label.pack(padx=20, pady=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.get_quote_button = tk.Button(self.button_frame, text="Get Random Quote", command=self.get_quote)
        self.get_quote_button.pack(side=tk.LEFT, padx=10)

        self.copy_quote_button = tk.Button(self.button_frame, text="Copy Quote", command=self.copy_quote)
        self.copy_quote_button.pack(side=tk.LEFT, padx=10)

        self.clear_quote_button = tk.Button(self.button_frame, text="Clear Quote", command=self.clear_quote)
        self.clear_quote_button.pack(side=tk.LEFT, padx=10)

        self.status_label = tk.Label(self.root, text="", font=("Arial", 10))
        self.status_label.pack(pady=10)

        self.get_quote()

    def get_quote(self):
        try:
            response = requests.get("https://zenquotes.io/api/random")
            response.raise_for_status()
            data = response.json()
            quote = data[0]["q"]
            author = data[0]["a"]

            self.quote_label.config(text=quote)
            self.author_label.config(text=f"- {author}")
            self.status_label.config(text="Quote fetched successfully!")
        except requests.exceptions.RequestException as e:
            self.quote_label.config(text="Error: " + str(e))
            self.author_label.config(text="")
            self.status_label.config(text="Failed to fetch quote.")

    def copy_quote(self):
        try:
            quote = self.quote_label.cget("text")
            author = self.author_label.cget("text")
            if quote and author:
                self.root.clipboard_clear()
                self.root.clipboard_append(f"{quote}\n{author}")
                self.status_label.config(text="Quote copied to clipboard!")
            else:
                self.status_label.config(text="No quote to copy.")
        except Exception as e:
            self.status_label.config(text="Error: " + str(e))

    def clear_quote(self):
        self.quote_label.config(text="")
        self.author_label.config(text="")
        self.status_label.config(text="Quote cleared.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    generator = Quo-teGenerator()
    generator.run()