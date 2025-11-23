import tkinter as tk
from tkinter import messagebox
import wikipedia

class WikipediaScanner:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Wikipedia Scanner")

        self.search_label = tk.Label(self.root, text="Enter Search Term:")
        self.search_label.pack()

        self.search_entry = tk.Entry(self.root, width=50)
        self.search_entry.pack()

        self.search_button = tk.Button(self.root, text="Search", command=self.search_wikipedia)
        self.search_button.pack()

        self.result_text = tk.Text(self.root, height=20, width=60)
        self.result_text.pack()

    def search_wikipedia(self):
        search_term = self.search_entry.get()
        try:
            result = wikipedia.summary(search_term)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
        except wikipedia.exceptions.DisambiguationError:
            messagebox.showerror("Error", "Disambiguation Error: Please specify a more precise search term")
        except wikipedia.exceptions.PageError:
            messagebox.showerror("Error", "Page Error: No page found for the given search term")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    scanner = WikipediaScanner()
    scanner.run()