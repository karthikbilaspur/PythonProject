import tkinter as tk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
import nltk
from tkinter import filedialog, messagebox
nltk.download('punkt')
nltk.download('stopwords')

class TextSummarizerGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Text Summarizer")

        # Create input label and text box
        self.input_label = tk.Label(self.window, text="Enter text:")
        self.input_label.pack()
        self.input_text = tk.Text(self.window, height=10, width=50)
        self.input_text.pack()

        # Create button to summarize text
        self.summarize_button = tk.Button(self.window, text="Summarize Text", command=self.summarize_text)
        self.summarize_button.pack()

        # Create button to load text file
        self.load_button = tk.Button(self.window, text="Load Text File", command=self.load_text_file)
        self.load_button.pack()

        # Create button to save summary
        self.save_button = tk.Button(self.window, text="Save Summary", command=self.save_summary)
        self.save_button.pack()

        # Create label to display summary
        self.summary_label = tk.Label(self.window, text="Summary:")
        self.summary_label.pack()
        self.summary_text = tk.Text(self.window, height=5, width=50)
        self.summary_text.pack()

    def summarize_text(self):
        # Get input text
        text = self.input_text.get("1.0", "end-1c")

        # Tokenize text into sentences
        sentences = sent_tokenize(text)

        # Tokenize text into words
        words = word_tokenize(text.lower())

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word not in stop_words]

        # Calculate word frequencies
        freq = FreqDist(words)

        # Calculate sentence scores
        scores = {}
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in freq:
                    if sentence in scores:
                        scores[sentence] += freq[word]
                    else:
                        scores[sentence] = freq[word]

        # Sort sentences by score
        sorted_sentences = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # Select top sentences
        top_sentences = [sentence[0] for sentence in sorted_sentences[:5]]

        # Join top sentences into summary
        summary = ' '.join(top_sentences)

        # Display summary
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert("1.0", summary)

    def load_text_file(self):
        # Open file dialog to select text file
        file_path = filedialog.askopenfilename(title="Select Text File", filetypes=[("Text Files", "*.txt")])

        # Read text from file
        if file_path:
            with open(file_path, 'r') as file:
                text = file.read()
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert("1.0", text)

    def save_summary(self):
        # Get summary text
        summary = self.summary_text.get("1.0", "end-1c")

        # Open file dialog to save summary
        file_path = filedialog.asksaveasfilename(title="Save Summary", defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

        # Save summary to file
        if file_path:
            with open(file_path, 'w') as file:
                file.write(summary)
            messagebox.showinfo("Success", "Summary saved successfully!")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    gui = TextSummarizerGUI()
    gui.run()