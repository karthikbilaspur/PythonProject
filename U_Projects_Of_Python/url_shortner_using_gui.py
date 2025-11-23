import tkinter as tk
from tkinter import messagebox
import pyshorteners

class URLShortener:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("URL Shortener")

        # Create input field
        self.url_label = tk.Label(self.window, text="Enter URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(self.window, width=50)
        self.url_entry.pack()

        # Create shorten button
        self.shorten_button = tk.Button(self.window, text="Shorten URL", command=self.shorten_url)
        self.shorten_button.pack()

        # Create label to display short URL
        self.short_url_label = tk.Label(self.window, text="")
        self.short_url_label.pack()

        # Create copy button
        self.copy_button = tk.Button(self.window, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.pack()
        self.copy_button.config(state="disabled")

    def shorten_url(self):
        long_url = self.url_entry.get().strip()
        if not long_url:
            messagebox.showerror("Error", "Please enter a URL")
            return

        try:
            shortener = pyshorteners.Shortener()
            short_url = shortener.tinyurl.short(long_url)
            self.short_url_label.config(text=f"Short URL: {short_url}")
            self.copy_button.config(state="normal")
            self.short_url = short_url
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def copy_to_clipboard(self):
        self.window.clipboard_clear()
        self.window.clipboard_append(self.short_url)
        messagebox.showinfo("Copied", "Short URL copied to clipboard!")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    url_shortener = URLShortener()
    url_shortener.run()