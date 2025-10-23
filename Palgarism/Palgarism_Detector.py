import tkinter as tk
from tkinter import filedialog, messagebox
from difflib import SequenceMatcher
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import docx
from PyPDF2 import PdfReader
import string

nltk.download('punkt')
nltk.download('stopwords')

class PlagiarismDetector:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Plagiarism Detector")

        # Create buttons to select files
        self.file1_button = tk.Button(self.window, text="Select File 1", command=self.select_file1)
        self.file1_button.pack()
        self.file1_label = tk.Label(self.window, text="No file selected")
        self.file1_label.pack()

        self.file2_button = tk.Button(self.window, text="Select File 2", command=self.select_file2)
        self.file2_button.pack()
        self.file2_label = tk.Label(self.window, text="No file selected")
        self.file2_label.pack()

        # Create options to ignore stop words and punctuation
        self.ignore_stop_words = tk.BooleanVar()
        self.ignore_stop_words_checkbox = tk.Checkbutton(self.window, text="Ignore stop words", variable=self.ignore_stop_words)
        self.ignore_stop_words_checkbox.pack()

        self.ignore_punctuation = tk.BooleanVar()
        self.ignore_punctuation_checkbox = tk.Checkbutton(self.window, text="Ignore punctuation", variable=self.ignore_punctuation)
        self.ignore_punctuation_checkbox.pack()

        # Create button to detect plagiarism
        self.detect_button = tk.Button(self.window, text="Detect Plagiarism", command=self.detect_plagiarism)
        self.detect_button.pack()

        # Create text area to display result
        self.result_text = tk.Text(self.window, height=20, width=60)
        self.result_text.pack()

        self.file1_path = None
        self.file2_path = None

    def select_file1(self):
        self.file1_path = filedialog.askopenfilename()
        self.file1_label['text'] = self.file1_path

    def select_file2(self):
        self.file2_path = filedialog.askopenfilename()
        self.file2_label['text'] = self.file2_path

    def read_file(self, file_path):
        if file_path.endswith('.txt'):
            with open(file_path, 'r') as file:
                return file.read()
        elif file_path.endswith('.docx'):
            doc = docx.Document(file_path)
            return '\n'.join([para.text for para in doc.paragraphs])
        elif file_path.endswith('.pdf'):
            reader = PdfReader(file_path)
            return '\n'.join([page.extract_text() for page in reader.pages])
        else:
            messagebox.showerror("Error", "Unsupported file format")
            return None

    def preprocess_text(self, text):
        stop_words = set(stopwords.words('english'))
        stemmer = PorterStemmer()

        words = word_tokenize(text.lower())
        words = [stemmer.stem(word) for word in words if word.isalpha()]

        if self.ignore_stop_words.get():
            words = [word for word in words if word not in stop_words]

        if self.ignore_punctuation.get():
            words = [word for word in words if word not in string.punctuation]

        return ' '.join(words)

    def detect_plagiarism(self):
        if self.file1_path is None or self.file2_path is None:
            messagebox.showerror("Error", "Please select both files")
            return

        try:
            file1_text = self.read_file(self.file1_path)
            file2_text = self.read_file(self.file2_path)

            if file1_text is None or file2_text is None:
                return

            file1_text = self.preprocess_text(file1_text)
            file2_text = self.preprocess_text(file2_text)

            similarity_ratio = SequenceMatcher(None, file1_text, file2_text).ratio()
            plagiarism_percentage = similarity_ratio * 100

            result = f"Plagiarism detected: {plagiarism_percentage:.2f}%\n"
            if plagiarism_percentage > 70:
                result += "High similarity detected. Possible plagiarism."
            elif plagiarism_percentage > 40:
                result += "Moderate similarity detected. Possible partial plagiarism."
            else:
                result += "Low similarity detected. No plagiarism detected."

            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    detector = PlagiarismDetector()
    detector.run()