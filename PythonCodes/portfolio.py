import tkinter as tk
from tkinter import ttk
import feedparser
import webbrowser

class MediumPortfolioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Medium Portfolio App")
        self.feed_url = "https://medium.com/feed/@your-medium-username"
        self.entries = []

        self.feed = feedparser.parse(self.feed_url)
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.frame = tk.Frame(self.notebook)
        self.notebook.add(self.frame, text="Articles")

        self.listbox = tk.Listbox(self.frame, width=100)
        self.listbox.pack(pady=10, expand=True, fill="both")

        for entry in self.feed.entries:
            self.listbox.insert(tk.END, entry.title)
            self.entries.append(entry)

        self.view_button = tk.Button(self.frame, text="View Article", command=self.view_article)
        self.view_button.pack(pady=10)

    def view_article(self):
        selected_index = self.listbox.curselection()[0]
        selected_entry = self.entries[selected_index]
        webbrowser.open(selected_entry.link)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MediumPortfolioApp(root)
    app.run()