import itertools
from collections import Counter
from typing import Optional
import tkinter as tk
from tkinter import filedialog, messagebox

def find_anagrams_fast(
    word: str,
    min_length: int = 1,
    max_length: Optional[int] = None,
    dict_words: Optional[set[str]] = None,
) -> set[str]:
    word = word.replace(" ", "").lower()
    if not word:
        return set()
    
    if max_length is None:
        max_length = len(word)

    word_counter = Counter(word)

    # If we have a dictionary, just filter the dictionary. WAY faster.
    if dict_words is not None:
        result: set[str] = set()
        for dw in dict_words:
            if not (min_length <= len(dw) <= max_length):
                continue
            # can this dict word be made from our letters?
            if not (Counter(dw) - word_counter):
                result.add(dw)
        return result

    # No dictionary - have to generate permutations (keep this for small words only)
    if len(word) > 8:
        raise ValueError(f"Word too long ({len(word)} chars) to generate without a dictionary. It would create millions of combos.")

    perms: set[str] = set()
    for r in range(min_length, max_length + 1):
        for p in itertools.permutations(word, r):
            perms.add(''.join(p))
    return perms

def load_dictionary(file_path: str) -> set[str]:
    with open(file_path, 'r', encoding='utf-8') as f:
        return {line.strip().lower() for line in f if line.strip()}

# --- GUI CLASS (Fixed) ---
class AnagramFinder:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Anagram Finder")
        
        input_frame = tk.Frame(self.window)
        input_frame.pack(padx=10, pady=10)
        tk.Label(input_frame, text="Enter a word:").pack(side=tk.LEFT)
        self.word_entry = tk.Entry(input_frame, width=30)
        self.word_entry.pack(side=tk.LEFT)

        length_frame = tk.Frame(self.window)
        length_frame.pack(padx=10, pady=10)
        tk.Label(length_frame, text="Min:").pack(side=tk.LEFT)
        self.min_length_entry = tk.Entry(length_frame, width=5)
        self.min_length_entry.insert(0, "1")
        self.min_length_entry.pack(side=tk.LEFT)
        tk.Label(length_frame, text="Max:").pack(side=tk.LEFT)
        self.max_length_entry = tk.Entry(length_frame, width=5)
        self.max_length_entry.pack(side=tk.LEFT)

        dict_frame = tk.Frame(self.window)
        dict_frame.pack(padx=10, pady=10)
        tk.Label(dict_frame, text="Dictionary:").pack(side=tk.LEFT)
        self.dictionary_entry = tk.Entry(dict_frame, width=30)
        self.dictionary_entry.pack(side=tk.LEFT)
        tk.Button(dict_frame, text="Browse", command=self.browse_dictionary).pack(side=tk.LEFT)

        tk.Button(self.window, text="Find Anagrams", command=self.find_anagrams).pack(pady=10)

        self.output_text = tk.Text(self.window, width=50, height=20)
        self.output_text.pack(padx=10, pady=10)

    def browse_dictionary(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        self.dictionary_entry.delete(0, tk.END)
        self.dictionary_entry.insert(0, file_path)

    def find_anagrams(self):
        word = self.word_entry.get()
        try:
            min_len = int(self.min_length_entry.get() or 1)
            max_len_str = self.max_length_entry.get()
            max_len = int(max_len_str) if max_len_str else None
        except ValueError:
            messagebox.showerror("Error", "Invalid length")
            return

        dict_file = self.dictionary_entry.get()
        dict_words = None
        if dict_file:
            try:
                dict_words = load_dictionary(dict_file)
            except FileNotFoundError:
                messagebox.showerror("Error", "Dictionary file not found")
                return
        
        try:
            anagrams = find_anagrams_fast(word, min_len, max_len, dict_words)
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, f"Found {len(anagrams)} anagrams:\n")
            for a in sorted(anagrams):
                self.output_text.insert(tk.END, a + "\n")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    # Change this to run CLI or GUI
    USE_GUI = True
    if USE_GUI:
        AnagramFinder().run()
    else:
        word = input("Enter a word: ")
        anagrams = find_anagrams_fast(word, dict_words=load_dictionary("words.txt") if input("Use dict? y/n ") == "y" else None)
        print(anagrams)