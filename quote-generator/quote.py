import tkinter as tk
from tkinter import messagebox
import requests
import json
import pyperclip

class QuoteGenerator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Quote Generator")

        self.quote_label = tk.Label(self.window, text="", wraplength=400, font=("Arial", 14))
        self.quote_label.pack(padx=20, pady=20)

        self.author_label = tk.Label(self.window, text="", font=("Arial", 12))
        self.author_label.pack(padx=20, pady=10)

        self.generate_button = tk.Button(self.window, text="Generate Quote", command=self.generate_quote)
        self.generate_button.pack(padx=20, pady=10)

        self.copy_button = tk.Button(self.window, text="Copy Quote", command=self.copy_quote)
        self.copy_button.pack(padx=20, pady=5)

        self.share_button = tk.Button(self.window, text="Share on Twitter", command=self.share_on_twitter)
        self.share_button.pack(padx=20, pady=5)

        self.generate_quote()

    def generate_quote(self):
        try:
            response = requests.get("https://api.quotable.io/random")
            response.raise_for_status()
            data = json.loads(response.text)
            self.quote = data["content"]
            self.author = data["author"]
            self.quote_label.config(text=self.quote)
            self.author_label.config(text=f"- {self.author}")
        except requests.RequestException as e:
            messagebox.showerror("Error", str(e))

    def copy_quote(self):
        try:
            pyperclip.copy(f'"{self.quote}" - {self.author}')
            messagebox.showinfo("Success", "Quote copied to clipboard")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def share_on_twitter(self):
        try:
            import webbrowser
            url = f"https://twitter.com/intent/tweet?text={self.quote} - {self.author}"
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    quote_generator = QuoteGenerator()
    quote_generator.run()