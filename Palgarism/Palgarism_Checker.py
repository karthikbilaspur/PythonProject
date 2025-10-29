import tkinter as tk
from tkinter import filedialog, messagebox
import difflib
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import requests

nltk.download('punkt')
nltk.download('stopwords')

class PlagiarismChecker:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Plagiarism Checker")

        # Create input field for text
        self.text_label = tk.Label(self.window, text="Enter Text:")
        self.text_label.pack()
        self.text_entry = tk.Text(self.window, height=10, width=40)
        self.text_entry.pack()

        # Create button to check plagiarism
        self.check_button = tk.Button(self.window, text="Check Plagiarism", command=self.check_plagiarism)
        self.check_button.pack()

        # Create button to check plagiarism from file
        self.file_button = tk.Button(self.window, text="Check Plagiarism from File", command=self.check_plagiarism_from_file)
        self.file_button.pack()

        # Create button to check plagiarism from URL
        self.url_button = tk.Button(self.window, text="Check Plagiarism from URL", command=self.check_plagiarism_from_url)
        self.url_button.pack()

        # Create text area to display result
        self.result_text = tk.Text(self.window, height=10, width=40)
        self.result_text.pack()

    def check_plagiarism(self):
        text1 = self.text_entry.get('1.0', tk.END)
        text2 = self.get_comparison_text()
        if text2:
            similarity = self.calculate_similarity(text1, text2)
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, f"Similarity: {similarity * 100}%")

    def check_plagiarism_from_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                text1 = file.read()
                text2 = self.get_comparison_text()
                if text2:
                    similarity = self.calculate_similarity(text1, text2)
                    self.result_text.delete('1.0', tk.END)
                    self.result_text.insert(tk.END, f"Similarity: {similarity * 100}%")

    def check_plagiarism_from_url(self):
        url = self.get_comparison_url()
        if url:
            try:
                response = requests.get(url)
                text1 = self.text_entry.get('1.0', tk.END)
                text2 = response.text
                similarity = self.calculate_similarity(text1, text2)
                self.result_text.delete('1.0', tk.END)
                self.result_text.insert(tk.END, f"Similarity: {similarity * 100}%")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def get_comparison_text(self):
        comparison_window = tk.Toplevel(self.window)
        comparison_window.title("Enter Comparison Text")

        comparison_label = tk.Label(comparison_window, text="Enter Comparison Text:")
        comparison_label.pack()
        comparison_entry = tk.Text(comparison_window, height=10, width=40)
        comparison_entry.pack()

        def get_text():
            text = comparison_entry.get('1.0', tk.END)
            comparison_window.destroy()
            return text

        get_button = tk.Button(comparison_window, text="OK", command=lambda: [f for f in [get_text()]])
        get_button.pack()
        self.window.wait_window(comparison_window)
        try:
            return comparison_entry.get('1.0', tk.END)
        except:
            return None

    def get_comparison_url(self):
        comparison_window = tk.Toplevel(self.window)
        comparison_window.title("Enter Comparison URL")

        comparison_label = tk.Label(comparison_window, text="Enter Comparison URL:")
        comparison_label.pack()
        comparison_entry = tk.Entry(comparison_window)
        comparison_entry.pack()

        def get_url():
            url = comparison_entry.get()
            comparison_window.destroy()
            return url

        get_button = tk.Button(comparison_window, text="OK", command=lambda: [f for f in [get_url()]])
        get_button.pack()
        self.window.wait_window(comparison_window)
        try:
            return comparison_entry.get()
        except:
            return None

    def calculate_similarity(self, text1: str, text2: str) -> float:
        tokens1 = word_tokenize(text1.lower())
        tokens2 = word_tokenize(text2.lower())

        stop_words = set(stopwords.words('english'))
        tokens1 = [token for token in tokens1 if token not in stop_words]
        tokens2 = [token for token in tokens2 if token not in stop_words]

        similarity = difflib.SequenceMatcher(None, ' '.join(tokens1), ' '.join(tokens2)).ratio()
        return similarity

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    checker = PlagiarismChecker()
    checker.run()