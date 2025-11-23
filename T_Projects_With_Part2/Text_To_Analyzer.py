import re
from collections import Counter
import tkinter as tk
from tkinter import filedialog, messagebox

class TextFileAnalyser:
    def __init__(self):
        self.file_path = None
        self.text = None

    def open_file(self):
        self.file_path = filedialog.askopenfilename(title="Select Text File", filetypes=[("Text Files", "*.txt")])
        if self.file_path:
            with open(self.file_path, 'r') as file:
                self.text = file.read()
            messagebox.showinfo("Success", "File opened successfully!")

    def count_words(self):
        if self.text:
            words = re.findall(r'\b\w+\b', self.text.lower())
            return len(words)
        else:
            return 0

    def count_unique_words(self):
        if self.text:
            words = re.findall(r'\b\w+\b', self.text.lower())
            return len(set(words))
        else:
            return 0

    def most_common_words(self, n=10):
        if self.text:
            words = re.findall(r'\b\w+\b', self.text.lower())
            return Counter(words).most_common(n)
        else:
            return []

    def word_frequency(self, word):
        if self.text:
            words = re.findall(r'\b\w+\b', self.text.lower())
            return words.count(word.lower())
        else:
            return 0

    def sentence_count(self):
        if self.text:
            sentences = re.split(r'[.!?]', self.text)
            return len([sentence for sentence in sentences if sentence.strip()])
        else:
            return 0

    def character_count(self):
        if self.text:
            return len(self.text)
        else:
            return 0

def main():
    root = tk.Tk()
    root.title("Text File Analyser")

    analyser = TextFileAnalyser()

    tk.Button(root, text="Open File", command=analyser.open_file).pack()

    tk.Label(root, text="Word Count:").pack()
    word_count_label = tk.Label(root, text="0")
    word_count_label.pack()

    tk.Label(root, text="Unique Word Count:").pack()
    unique_word_count_label = tk.Label(root, text="0")
    unique_word_count_label.pack()

    tk.Label(root, text="Most Common Words:").pack()
    most_common_words_label = tk.Label(root, text="")
    most_common_words_label.pack()

    tk.Label(root, text="Word Frequency:").pack()
    word_frequency_frame = tk.Frame(root)
    word_frequency_frame.pack()
    word_entry = tk.Entry(word_frequency_frame, width=10)
    word_entry.pack(side=tk.LEFT)
    word_frequency_label = tk.Label(word_frequency_frame, text="0")
    word_frequency_label.pack(side=tk.LEFT)

    tk.Label(root, text="Sentence Count:").pack()
    sentence_count_label = tk.Label(root, text="0")
    sentence_count_label.pack()

    tk.Label(root, text="Character Count:").pack()
    character_count_label = tk.Label(root, text="0")
    character_count_label.pack()

    def update_stats():
        if analyser.text:
            word_count_label['text'] = str(analyser.count_words())
            unique_word_count_label['text'] = str(analyser.count_unique_words())
            most_common_words_label['text'] = str(analyser.most_common_words())
            sentence_count_label['text'] = str(analyser.sentence_count())
            character_count_label['text'] = str(analyser.character_count())

    def get_word_frequency():
        word = word_entry.get()
        if word:
            word_frequency_label['text'] = str(analyser.word_frequency(word))

    tk.Button(root, text="Update Stats", command=update_stats).pack()
    tk.Button(word_frequency_frame, text="Get Frequency", command=get_word_frequency).pack(side=tk.LEFT)

    root.mainloop()

if __name__ == "__main__":
    main()