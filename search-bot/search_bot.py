"""
Search Bot — fetch a page, summarise it, make a word cloud, save it.
Fixes vs original:
- gensim.summarization was REMOVED in gensim 4.x, so this uses a small
  built-in extractive summariser (no gensim needed) — no ImportError.
- Scraping Google/Bing HTML is blocked / against ToS and returns junk.
  This version fetches a URL you paste (e.g. a Wikipedia/article URL)
  instead of pretending to scrape a search engine.
- Adds a User-Agent header, timeout, and empty-text guard.

Requires: pip install requests beautifulsoup4 wordcloud matplotlib
"""
import re
import tkinter as tk
from tkinter import filedialog, messagebox

import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud

HEADERS = {"User-Agent": "Mozilla/5.0 (SearchBot demo/1.0)"}


def extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()
    text = soup.get_text(separator=" ")
    return re.sub(r"\s+", " ", text).strip()


def extractive_summary(text: str, ratio: float = 0.1) -> str:
    """Pick the highest-scoring sentences by word frequency. Simple, dependency-free."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 30]
    if not sentences:
        return text[:2000]
    words = re.findall(r"[a-z]+", text.lower())
    stop = set("the a an and or of to in on for with is are was were be been it this that by at as from".split())
    freq = {}
    for w in words:
        if w not in stop:
            freq[w] = freq.get(w, 0) + 1
    scored = []
    for i, s in enumerate(sentences):
        score = sum(freq.get(w, 0) for w in re.findall(r"[a-z]+", s.lower()))
        scored.append((score / max(len(s.split()), 1), i, s))
    n = max(1, int(len(sentences) * ratio))
    picked = sorted(sorted(scored, reverse=True)[:n], key=lambda x: x[1])
    return " ".join(s for _, _, s in picked)


class SearchBot:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Search Bot")
        self.root.geometry("600x520")

        tk.Label(self.root, text="Enter Article / Page URL:", font=("Arial", 13)).pack(pady=8)
        self.url_entry = tk.Entry(self.root, width=55, font=("Arial", 12))
        self.url_entry.pack(pady=4)
        self.url_entry.insert(0, "https://en.wikipedia.org/wiki/Python_(programming_language)")

        tk.Label(self.root, text="Summary Length (0-1):", font=("Arial", 13)).pack(pady=8)
        self.length_entry = tk.Entry(self.root, width=10, font=("Arial", 12))
        self.length_entry.insert(0, "0.1")
        self.length_entry.pack()

        btns = tk.Frame(self.root); btns.pack(pady=10)
        tk.Button(btns, text="Fetch + Summarise", command=self.search, font=("Arial", 12)).pack(side=tk.LEFT, padx=6)
        tk.Button(btns, text="Word Cloud", command=self.generate_wordcloud, font=("Arial", 12)).pack(side=tk.LEFT, padx=6)
        tk.Button(btns, text="Save Summary", command=self.save_summary, font=("Arial", 12)).pack(side=tk.LEFT, padx=6)

        tk.Label(self.root, text="Summary:", font=("Arial", 13)).pack()
        self.summary_text = tk.Text(self.root, height=12, width=60, font=("Arial", 11))
        self.summary_text.pack(pady=6)

    def search(self):
        try:
            ratio = float(self.length_entry.get())
            if not 0 < ratio <= 1:
                raise ValueError("Ratio must be between 0 and 1")
            url = self.url_entry.get().strip()
            if not url.startswith("http"):
                raise ValueError("Enter a full URL starting with http:// or https://")
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            text = extract_text(resp.text)
            if len(text) < 200:
                raise ValueError("Page returned very little readable text (may be JS-rendered or blocked).")
            summary = extractive_summary(text, ratio)
            self.summary_text.delete("1.0", tk.END)
            self.summary_text.insert(tk.END, summary)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def generate_wordcloud(self):
        try:
            summary = self.summary_text.get("1.0", tk.END).strip()
            if not summary:
                raise ValueError("Fetch a summary first.")
            wc = WordCloud(width=900, height=600, background_color="white").generate(summary)
            plt.figure(figsize=(10, 7)); plt.imshow(wc, interpolation="bilinear"); plt.axis("off"); plt.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_summary(self):
        try:
            summary = self.summary_text.get("1.0", tk.END)
            path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if path:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(summary)
                messagebox.showinfo("Success", "Summary saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    SearchBot().run()
