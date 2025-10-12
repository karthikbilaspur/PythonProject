import re
from collections import Counter
import tkinter as tk
from tkinter import filedialog

class NgramGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("N-gram Generator")

        # Create GUI widgets
        self.text_label = tk.Label(root, text="Enter text:")
        self.text_label.pack()
        self.text_box = tk.Text(root, height=10, width=40)
        self.text_box.pack()
        self.n_label = tk.Label(root, text="Enter n:")
        self.n_label.pack()
        self.n_entry = tk.Entry(root)
        self.n_entry.pack()
        self.generate_button = tk.Button(root, text="Generate N-grams", command=self.generate_ngrams)
        self.generate_button.pack()
        self.result_label = tk.Label(root, text="Result:")
        self.result_label.pack()
        self.result_box = tk.Text(root, height=10, width=40)
        self.result_box.pack()
        self.save_button = tk.Button(root, text="Save to file", command=self.save_to_file)
        self.save_button.pack()
        self.open_button = tk.Button(root, text="Open file", command=self.open_file)
        self.open_button.pack()

    def generate_ngrams(self):
        text = self.text_box.get("1.0", tk.END)
        n = int(self.n_entry.get())
        ngrams = self.calculate_ngrams(text, n)
        self.result_box.delete("1.0", tk.END)
        for ngram in ngrams:
            self.result_box.insert(tk.END, ngram + "\n")

    def calculate_ngrams(self, text, n):
        # Tokenize the text into words
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Generate n-grams
        ngrams = []
        for i in range(len(words) - n + 1):
            ngram = ' '.join(words[i:i+n])
            ngrams.append(ngram)
        
        return ngrams

    def save_to_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt")
        if filename:
            with open(filename, "w") as file:
                file.write(self.result_box.get("1.0", tk.END))

    def open_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            with open(filename, "r") as file:
                self.text_box.delete("1.0", tk.END)
                self.text_box.insert(tk.END, file.read())

if __name__ == "__main__":
    root = tk.Tk()
    app = NgramGenerator(root)
    root.mainloop()