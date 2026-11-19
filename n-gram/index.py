import re
from collections import Counter
import tkinter as tk
from tkinter import filedialog, messagebox

class NgramGenerator:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.title("N-gram Generator")
        self.root.geometry("500x650")
        self.root.resizable(False, False)

        # Input text
        self.text_label = tk.Label(root, text="Enter text:")
        self.text_label.pack(pady=(10, 0), anchor="w", padx=10)
        self.text_box = tk.Text(root, height=10, width=60)
        self.text_box.pack(padx=10)

        # N input
        self.n_frame = tk.Frame(root)
        self.n_frame.pack(pady=10)
        self.n_label = tk.Label(self.n_frame, text="Enter n:")
        self.n_label.pack(side=tk.LEFT, padx=(0, 5))
        self.n_entry = tk.Entry(self.n_frame, width=5)
        self.n_entry.pack(side=tk.LEFT)
        self.n_entry.insert(0, "2")

        # Show counts checkbox
        self.show_counts = tk.BooleanVar(value=True)
        self.counts_check = tk.Checkbutton(
            root, text="Show frequencies (most common first)",
            variable=self.show_counts
        )
        self.counts_check.pack()

        # Generate button
        self.generate_button = tk.Button(
            root, text="Generate N-grams", command=self.generate_ngrams
        )
        self.generate_button.pack(pady=5)

        # Result
        self.result_label = tk.Label(root, text="Result:")
        self.result_label.pack(anchor="w", padx=10)
        self.result_box = tk.Text(root, height=12, width=60)
        self.result_box.pack(padx=10)

        # File buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)
        self.save_button = tk.Button(
            self.button_frame, text="Save to file", command=self.save_to_file
        )
        self.save_button.pack(side=tk.LEFT, padx=5)
        self.open_button = tk.Button(
            self.button_frame, text="Open file", command=self.open_file
        )
        self.open_button.pack(side=tk.LEFT, padx=5)
        self.clear_button = tk.Button(
            self.button_frame, text="Clear all", command=self.clear_all
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)

    def generate_ngrams(self):
        text = self.text_box.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("No text", "Please enter some text first.")
            return

        try:
            n = int(self.n_entry.get())
            if n < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid n", "Please enter a positive integer for n.")
            return

        counts = self.calculate_ngrams(text, n)

        self.result_box.delete("1.0", tk.END)

        if not counts:
            self.result_box.insert(
                tk.END,
                f"Not enough words for n={n}.\n"
                f"Your text has fewer than {n} words."
            )
            return

        if self.show_counts.get():
            for ngram, count in counts.most_common():
                self.result_box.insert(tk.END, f"{count} x {ngram}\n")
        else:
            # Show each n-gram once, in order of appearance
            seen: set[str] = set()
            words = re.findall(r'\b\w+\b', text.lower())
            for i in range(len(words) - n + 1):
                ngram = ' '.join(words[i:i + n])
                if ngram not in seen:
                    seen.add(ngram)
                    self.result_box.insert(tk.END, f"{ngram}\n")

    def calculate_ngrams(self, text: str, n: int) -> Counter[str]:
        # Tokenize the text into words
        words = re.findall(r'\b\w+\b', text.lower())

        if len(words) < n:
            return Counter()

        # Generate n-grams and count them
        ngrams = [
            ' '.join(words[i:i + n])
            for i in range(len(words) - n + 1)
        ]
        return Counter(ngrams)

    def save_to_file(self):
        content = self.result_box.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Nothing to save", "Result box is empty.")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(content)
                messagebox.showinfo("Saved", f"Saved to {filename}")
            except OSError as e:
                messagebox.showerror("Save failed", str(e))

    def open_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, "r", encoding="utf-8") as file:
                    self.text_box.delete("1.0", tk.END)
                    self.text_box.insert(tk.END, file.read())
            except OSError as e:
                messagebox.showerror("Open failed", str(e))

    def clear_all(self):
        self.text_box.delete("1.0", tk.END)
        self.result_box.delete("1.0", tk.END)
        self.n_entry.delete(0, tk.END)
        self.n_entry.insert(0, "2")

if __name__ == "__main__":
    root = tk.Tk()
    app = NgramGenerator(root)
    root.mainloop()