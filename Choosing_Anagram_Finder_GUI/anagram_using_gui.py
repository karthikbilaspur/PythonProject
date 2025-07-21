import tkinter as tk
from tkinter import filedialog, messagebox
import itertools

class AnagramFinder:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Anagram Finder")

        # Input frame
        self.input_frame = tk.Frame(self.window)
        self.input_frame.pack(padx=10, pady=10)

        tk.Label(self.input_frame, text="Enter a word:").pack(side=tk.LEFT)
        self.word_entry = tk.Entry(self.input_frame, width=30)
        self.word_entry.pack(side=tk.LEFT)

        # Length frame
        self.length_frame = tk.Frame(self.window)
        self.length_frame.pack(padx=10, pady=10)

        tk.Label(self.length_frame, text="Minimum length:").pack(side=tk.LEFT)
        self.min_length_entry = tk.Entry(self.length_frame, width=5)
        self.min_length_entry.insert(0, "0")
        self.min_length_entry.pack(side=tk.LEFT)

        tk.Label(self.length_frame, text="Maximum length:").pack(side=tk.LEFT)
        self.max_length_entry = tk.Entry(self.length_frame, width=5)
        self.max_length_entry.pack(side=tk.LEFT)

        # Dictionary frame
        self.dictionary_frame = tk.Frame(self.window)
        self.dictionary_frame.pack(padx=10, pady=10)

        tk.Label(self.dictionary_frame, text="Dictionary file:").pack(side=tk.LEFT)
        self.dictionary_entry = tk.Entry(self.dictionary_frame, width=30)
        self.dictionary_entry.pack(side=tk.LEFT)
        tk.Button(self.dictionary_frame, text="Browse", command=self.browse_dictionary).pack(side=tk.LEFT)

        # Button frame
        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(padx=10, pady=10)

        tk.Button(self.button_frame, text="Find Anagrams", command=self.find_anagrams).pack(side=tk.LEFT)

        # Output frame
        self.output_frame = tk.Frame(self.window)
        self.output_frame.pack(padx=10, pady=10)

        self.output_text = tk.Text(self.output_frame, width=50, height=20)
        self.output_text.pack(side=tk.LEFT)

    def browse_dictionary(self):
        file_path = filedialog.askopenfilename(title="Select Dictionary File", filetypes=[("Text Files", "*.txt")])
        self.dictionary_entry.delete(0, tk.END)
        self.dictionary_entry.insert(0, file_path)

    def find_anagrams(self):
        word = self.word_entry.get().replace(" ", "").lower()
        try:
            min_length = int(self.min_length_entry.get())
            max_length = self.max_length_entry.get()
            if max_length:
                max_length = int(max_length)
            else:
                max_length = len(word)
        except ValueError:
            messagebox.showerror("Error", "Invalid length")
            return

        dictionary_file = self.dictionary_entry.get()
        if dictionary_file:
            try:
                with open(dictionary_file, 'r') as f:
                    dict_words = set(word.strip().lower() for word in f)
            except FileNotFoundError:
                messagebox.showerror("Error", "Dictionary file not found")
                return
        else:
            dict_words = None

        anagrams = self.generate_anagrams(word, min_length, max_length, dict_words)
        self.output_text.delete('1.0', tk.END)
        for anagram in anagrams:
            self.output_text.insert(tk.END, anagram + "\n")

    def generate_anagrams(self, word, min_length, max_length, dict_words=None):
        perms = [''.join(p) for r in range(min_length, max_length + 1) 
                 for p in itertools.permutations(word, r)]
        anagrams = set(perms)
        if dict_words:
            anagrams = anagrams & dict_words
        return anagrams

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = AnagramFinder()
    app.run()