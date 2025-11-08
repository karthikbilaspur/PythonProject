import tkinter as tk
from bs4 import BeautifulSoup
import requests
from gensim.summarization import summarize
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from tkinter import messagebox, filedialog

class SearchBot:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Search Bot")
        self.root.geometry("600x500")

        self.query_label = tk.Label(self.root, text="Enter Search Query:", font=("Arial", 14))
        self.query_label.pack(pady=10)

        self.query_entry = tk.Entry(self.root, width=50, font=("Arial", 14))
        self.query_entry.pack(pady=10)

        self.engine_label = tk.Label(self.root, text="Select Search Engine:", font=("Arial", 14))
        self.engine_label.pack(pady=10)

        self.engine_var = tk.StringVar()
        self.engine_var.set("Google")
        self.engine_menu = tk.OptionMenu(self.root, self.engine_var, "Google", "Bing", "DuckDuckGo")
        self.engine_menu.pack(pady=10)

        self.length_label = tk.Label(self.root, text="Summary Length (0-1):", font=("Arial", 14))
        self.length_label.pack(pady=10)

        self.length_entry = tk.Entry(self.root, width=10, font=("Arial", 14))
        self.length_entry.insert(0, "0.1")
        self.length_entry.pack(pady=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.submit_button = tk.Button(self.button_frame, text="Submit", command=self.search, font=("Arial", 14))
        self.submit_button.pack(side=tk.LEFT, padx=10)

        self.wordcloud_button = tk.Button(self.button_frame, text="Generate Word Cloud", command=self.generate_wordcloud, font=("Arial", 14))
        self.wordcloud_button.pack(side=tk.LEFT, padx=10)

        self.save_button = tk.Button(self.button_frame, text="Save Summary", command=self.save_summary, font=("Arial", 14))
        self.save_button.pack(side=tk.LEFT, padx=10)

        self.summary_label = tk.Label(self.root, text="Summary:", font=("Arial", 14))
        self.summary_label.pack(pady=10)

        self.summary_text = tk.Text(self.root, height=10, width=50, font=("Arial", 14))
        self.summary_text.pack(pady=10)

    def search(self):
        try:
            query = self.query_entry.get()
            engine = self.engine_var.get()
            length = float(self.length_entry.get())

            if engine == "Google":
                url = f"https://www.google.com/search?q={query}"
            elif engine == "Bing":
                url = f"https://www.bing.com/search?q={query}"
            elif engine == "DuckDuckGo":
                url = f"https://duckduckgo.com/?q={query}"

            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            summary = summarize(text, ratio=length)
            self.summary_text.delete(1.0, tk.END)
            self.summary_text.insert(tk.END, summary)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def generate_wordcloud(self):
        try:
            summary = self.summary_text.get("1.0", tk.END)
            wordcloud = WordCloud().generate(summary)
            plt.figure(figsize=(10, 8))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_summary(self):
        try:
            summary = self.summary_text.get("1.0", tk.END)
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if file_path:
                with open(file_path, "w") as file:
                    file.write(summary)
                messagebox.showinfo("Success", "Summary saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    bot = SearchBot()
    bot.run()