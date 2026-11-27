import tkinter as tk
from tkinter import filedialog, messagebox
import re
from collections import Counter

class TextFileAnalyser:
    def __init__(self):
        self.file_path = None
        self.text = None
    def open_file(self):
        p = filedialog.askopenfilename(title="Select Text File", filetypes=[("Text Files", "*.txt")])
        if p:
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                self.text = f.read()
                self.file_path = p
            return True
        return False
    def words(self):
        return re.findall(r"\b\w+\b", self.text.lower()) if self.text else []
    def count_words(self):
        return len(self.words())
    def count_unique_words(self):
        return len(set(self.words()))
    def most_common_words(self, n: int = 10):
        return Counter(self.words()).most_common(n)
    def word_frequency(self, word: str) -> int:
        return self.words().count(word.lower()) if self.text else 0
    def sentence_count(self):
        if not self.text:
            return 0
        return len([s for s in re.split(r"[.!?]+", self.text) if s.strip()])
    def character_count(self):
        return len(self.text) if self.text else 0

def open_analyser_window(parent: tk.Misc):
    win = tk.Toplevel(parent)
    win.title("Text File Analyser")
    win.geometry("520x560")
    analyser = TextFileAnalyser()
    file_label = tk.Label(win, text="No file loaded", fg="gray")
    file_label.pack(pady=5)
    labels: dict[str, tk.Label] = {}
    for name in ["Word Count", "Unique Word Count", "Most Common Words", "Sentence Count", "Character Count"]:
        tk.Label(win, text=name + ":").pack()
        lbl = tk.Label(win, text="0" if "Common" not in name else "", wraplength=480, justify="left")
        lbl.pack()
        labels[name] = lbl
    tk.Label(win, text="Word Frequency:").pack(pady=(10, 0))
    frame = tk.Frame(win)
    frame.pack()
    entry = tk.Entry(frame, width=15)
    entry.pack(side=tk.LEFT, padx=5)
    freq_label = tk.Label(frame, text="0")
    freq_label.pack(side=tk.LEFT)

    def update_stats():
        if not analyser.text:
            messagebox.showwarning("No file", "Open a text file first.")
            return
        labels["Word Count"].config(text=str(analyser.count_words()))
        labels["Unique Word Count"].config(text=str(analyser.count_unique_words()))
        labels["Most Common Words"].config(text=str(analyser.most_common_words()))
        labels["Sentence Count"].config(text=str(analyser.sentence_count()))
        labels["Character Count"].config(text=str(analyser.character_count()))

    def open_and_update():
        if analyser.open_file():
            file_label.config(text=analyser.file_path or "", fg="black")
            update_stats()

    def get_freq():
        w = entry.get().strip()
        if w:
            freq_label.config(text=str(analyser.word_frequency(w)))

    tk.Button(win, text="Open File", command=open_and_update).pack(pady=8)
    tk.Button(win, text="Update Stats", command=update_stats).pack(pady=3)
    tk.Button(frame, text="Get Frequency", command=get_freq).pack(side=tk.LEFT, padx=5)
